from flask import (Flask,
                    request,
                    abort,
                    render_template
)

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage, # 傳輸回Line官方後台的資料格式
    ImageMessage
)
from linebot.v3.webhooks import (
    MessageEvent, # 傳輸過來的方法
    TextMessageContent,  # 使用者傳過來的資料格式
    ImageMessageContent
)
import os
from handle_keys import get_secret_and_token
from openai_api import chat_with_chatgpt
from data_scraper.cwa_opendata_scraper import get_cities_weather

app = Flask(__name__)
keys=get_secret_and_token()
configuration = Configuration(access_token=keys["LINEBOT_ACCESS_TOKEN"])
handler = WebhookHandler(keys["LINEBOT_SECRET_KEY"])

@app.route("/")
def hello_world(username=""):
    #測試用，確定webhook server 有連通
    return render_template("hello.html",name=username)

@app.route("/callback", methods=['POST'])
def callback():
    # 設計一個 callback 的路由，提供給Line官方後台去呼叫
    # 也就是所謂的呼叫Webhook Srever
    # 因為官方會把使用者傳輸的訊息轉傳給Webhook Server
    # 所以會使用 RESTful API 的POST的方法
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    # 根據不同的使用者事件(event)，區分不同的方式回應
    # eg.MessageEvent 代表使用者單純傳訊息的事件
    # TextMessageContent 代表使用者傳輸的訊息內容是文字
    # 符合兩個條件的事件，會被 handle_message 所處理
    user_id=event.source.user_id #使用者的ID
    user_message = event.message.text # 使用者傳過來的訊息在這裡
    api_key=keys["OPENAI_API_KEY"]

    #天氣如何 臺中市
    if "天氣如何" in user_message:
        #問天氣
       response = handle_weather(user_id, user_message)
    else:
        #閒聊
        response = chat_with_chatgpt(user_id,user_message,api_key)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[
                    TextMessage(text=response)
                ]
            )
        )

def handle_weather(user_id, user_message, chatgpt_api_key=keys['OPENAI_API_KEY']):
    # 問天氣
    cwa_api_key = keys['CWA_API_KEY']
    locations_name = user_message.split()[1:]
    if locations_name: # 有地點才做事情
        weather_data = get_cities_weather(cwa_api_key, locations_name)
        '''
        台中市:
            xxx: aaa 
            yyy: bbb
            zzz: ccc
        '''
        response = ""
        for location in weather_data: # 取得每一個縣市的名稱
            response += f"{location}:\n" # 加入縣市名稱訊息到response
            for weather_key in sorted(weather_data[location]): # 根據縣市名稱，取得縣市天氣資料
                response += f"\t\t{weather_key}: {weather_data[location][weather_key]}\n"
        response = response.strip()
        response = chat_with_chatgpt(
            user_id, response, chatgpt_api_key,
            extra_prompt="請你幫我生出一段報導，根據前面的天氣資訊，建議使用者的穿搭等等，每個縣市分開，200字以內。"
        )
    else:
        response = "請給我你想知道的縣市，請輸入：天氣如何 臺中市 桃園市 彰化市"
    return response

import requests
@handler.add(MessageEvent, message=ImageMessageContent)
def handle_image(event):
    # 取得圖片
    image_id = event.message.id
    image_url = f'https://api-data.line.me/v2/bot/message/{image_id}/content'
    header = {'Authorization': f'Bearer {keys['LINEBOT_ACCESS_TOKEN']}'}
    # 存圖片
    response = requests.get(image_url, headers=header)

    if response.status_code == 200:
        with open("image_message.jpeg", "wb") as image_file:
            image_file.write(response.content)
        response = "Get image success"
    else:
        response = "Get image failed"

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text=response), TextMessage(text=response), TextMessage(text=response)]
            )
        )

if __name__ == "__main__":
    app.run(debug=True)