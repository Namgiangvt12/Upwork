from selenium import webdriver
from time import sleep
import csv
from selenium.webdriver.chrome.options import Options
import threading
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from MyClasses import LinkPDF

browsers = []
threads = []
lock = threading.Lock()
chrome_options = Options()
chrome_options.add_argument("--headless")
sleep(2)
links =[]
for i in range(1, 2):
    links.append(LinkPDF(f"https://www.centralbankbahamas.com/bank-supervision/warning-notices"))
def thread_task(url) :
    browser = webdriver.Chrome()
    browser.get(url)
    sleep(4)
    for i in range(1,1000) :
        try :
            linkElement = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located((By.XPATH,f'/html/body/div[5]/section[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody/tr[{i}]/td[1]/div/span/a')))
        except :
            print("cant find element")
            break
        link = linkElement.get_attribute("href")
        print(link)
    file_path = f'links_{i}.csv'
    #with lock:
        #with open(file_path, 'a', encoding="utf-8") as txt:
            #txt.write(f'{link}\n')
    browser.quit()


for link in links:
    thread = threading.Thread(target=thread_task, args=(link.URL,))
    thread.start()
    threads.append(thread)

# Chờ cho tất cả các luồng hoàn thành
for thread in threads:
    thread.join()
