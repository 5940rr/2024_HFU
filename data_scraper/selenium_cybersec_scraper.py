from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException

def create_webdriver():
    return webdriver.Firefox()


def get_exd_detail(url,driver):

    data=dict()    
    driver.get(url)

    #電話
    try:
        telephone_element=driver.find_element(By.CLASS_NAME,"info-tel")
        data["電話"]=telephone_element.text
    except NoSuchElementException:
        print(f"URL: {url}, has no telephone")

    #email
    try:
        email_element=driver.find_element(By.CLASS_NAME,"info-mail")
        data["信箱"]=email_element.text
    except NoSuchElementException:
        print(f"URL: {url}, has no email")

    #website
    website_elements=driver.find_elements(By.CLASS_NAME,"border-icon")

    if website_elements: # 確定有東西
        for website_element in website_elements:
            # 利用 element.get_attribute("屬性名稱") 取得資訊
            href=website_element.get_attribute("href")
            if href:
                for social_media_name in ["facebook","twitter","linkedin"]:
                    if social_media_name in href:
                        data[social_media_name]=href
                    else:
                        data["website"]=href
                
                #if "facebook" in href: # facebook這幾個字有無出現在連結
                #     data["facebook"]=href
                # elif "twitter" in href:
                #     data["twitter"]=href
                # elif "linkedin" in href:
                #     data["linkdin"]=href
                # else:
                #     data["website"]=href

    #Description
    try:
        Description_element=driver.find_element(By.CLASS_NAME,"ex-foreword")
        data["簡介"]=Description_element.text
    except NoSuchElementException:
        print(f"URL: {url}, has no Description")
    
    return data

if __name__=="__main__":
    driver = create_webdriver()
    url="https://cybersec.ithome.com.tw/2024/exhibition-page/2259"

    exd_data=get_exd_detail(url,driver)

    print(exd_data)
    driver.close()

