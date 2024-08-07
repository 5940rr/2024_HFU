from flask import Flask #在flask這個工具箱裡 使用Flask這個工具
from flask import redirect, url_for,render_template

app = Flask(__name__) #製作出一個由Flask類別生成的物件 (object)

@app.route("/")#裝飾器:根目錄要做啥事
def world():
    return "<p>hello world<p>"

@app.route("/<string:username>") 
def hello_world(username=""):
    return render_template("hello.html",name=username)

@app.route("/eat_<string:whatfruit>") #說出任意一種水果並導向到吃掉水果
def say_fruit(whatfruit):
    return redirect(url_for('eat_fruit',fruit=whatfruit))

@app.route("/eat/<string:fruit>") 
def eat_fruit(fruit):
    return "<p>""eat "+fruit+"<p>" 

#執行方法在終端機輸入: flask --app flask_linebot.py run
#debug模式          : flask --app flask_linebot.py --debug run

#如果我直接執行這個檔案，那__name__就等於__main__
if __name__=="__main__": 
    #第二種執行方法
    app.run(debug=True)

