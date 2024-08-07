from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Firefox()
url="https://www.railway.gov.tw/tra-tip-web/tip/tip001/tip121/query"
driver.get(url)

#輸入身分證
elem=driver.find_element(By.CLASS_NAME,"idmember.pid.form-input")
elem.clear()
elem.send_keys("L125626439")
time.sleep(3)

#輸入出發站
elem=driver.find_element(By.CLASS_NAME,"startStation.ui-autocomplete-input")
elem.clear()
elem.send_keys(input("請輸入出發站: "))
elem.send_keys(Keys.RETURN)
elem.send_keys(Keys.RETURN)
time.sleep(3)

#輸入抵達站
elem=driver.find_element(By.CLASS_NAME,"endStation.ui-autocomplete-input")
elem.clear()
elem.send_keys(input("請輸入抵達站: "))
elem.send_keys(Keys.RETURN)
elem.send_keys(Keys.RETURN)
time.sleep(3)

#選擇單程票
tickey=input("請輸入單程or去回: ")
one_way_ticket=driver.find_element(By.XPATH, "//input[@title='單程']")
return_ticket=driver.find_element(By.XPATH, "//input[@title='去回']")
if tickey == "單程" :
    one_way_ticket.click()
else:
    return_ticket.click()


driver.close()