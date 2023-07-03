from selenium import webdriver
from time import sleep

from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By


chrome_options = Options()
chrome_options.add_argument("--headless")  # Chạy trình duyệt ẩn danh
browser = webdriver.Chrome()
browser.get("https://services.ca.judiciary.gov.ph/recentdecisions/")
sleep(3)
select50 = browser.find_element(By.XPATH, "/html/body/center/div[3]/form/div/div[3]/select/option[4]")
select50.click()
sleep(1)
viewPDF = browser.find_element(By.XPATH,"/html/body/center/div[3]/form/div/div[2]/table/tbody/tr[1]/td[4]")
viewPDF.click()
sleep(2)
browser.find_element(By.XPATH,'/html/body').send_keys(Keys.CONTROL, 's')
page_content = browser.page_source

# Lưu nội dung vào tệp tin
with open('1.pdf', 'w', encoding='utf-8') as file:
    file.write(page_content)
sleep(10)
browser.quit()
