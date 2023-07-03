from selenium import webdriver
from time import sleep
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
browser = webdriver.Chrome()
url = f'https://www.asc.ca/en/issuer-regulation/decisions-and-orders#sort=%40z95xcreateddate%20descending&f:noticesdecisionstypefacetid=[Variation%20of%20Cease%20Trade%20Order,Management%20Cease%20Trade%20Order,Undertaking,Revocation%20Order,Undertaking%20Fulfilled,ASC%20Decision,Order,Interim%20Management%20Cease%20Trade%20Order,Settlement%20Agreement%2FUndertaking,Halt%20Trade%20Order,Variation%20Order,Interim%20Order]'
browser.get(url)
wait = WebDriverWait(browser, 10)
sleep(2)
elements = browser.find_elements(By.XPATH, f'/html/body/div/div/div/div[1]/div[2]/div[1]/div[2]/div[2]/div/div/div/div[3]/div[2]/div[8]/div/div[2]')

for pageDoc in range(1,101):

    for element in elements:
        for count in range(1,11) :
            docTittle = element.find_element(By.XPATH,
                                             f'//*[@id="coveoD983BA32"]/div[2]/div[{count}]/div/div/div/div/div/div[2]/div/div'
                                             )
            includeLink = element.find_element(By.XPATH,
                                             f'//*[@id="coveoD983BA32"]/div[2]/div[{count}]/div/div/div/div/div/div[2]/div/div/a'
                                             )
            hrefLink = includeLink.get_attribute("href")
            dateDoc = element.find_element(By.XPATH,
                                             f'//*[@id="coveoD983BA32"]/div[2]/div[{count}]/div/div/div/div/div/div[3]'
                                             )
            typeDoc = element.find_element(By.XPATH,
                                             f'//*[@id="coveoD983BA32"]/div[2]/div[{count}]/div/div/div/div/div/div[4]'
                                             )
            partiesInvolved = element.find_element(By.XPATH,
                                             f'//*[@id="coveoD983BA32"]/div[2]/div[{count}]/div/div/div/div/div/div[5]'
                                             )
            print(f"{docTittle.text},{hrefLink},{dateDoc.text},{typeDoc.text},\"{partiesInvolved.text}\"")
            file_path = '40.0092_2.csv'
            with open(file_path, 'a') as file:
                file.write(f"\"{docTittle.text}\",{hrefLink},{dateDoc.text},{typeDoc.text},\"{partiesInvolved.text}\"\n")
    print(f"Đang Đọc Tới Page thứ : {pageDoc}")
    if pageDoc == 1 :
        nextBtn = browser.find_element(By.XPATH,
                                          f'//*[@id="coveo248b211e"]/div[2]/div[2]/div/div/div/div[3]/div[2]/div[9]/ul/li[11]')
        browser.execute_script("arguments[0].click();", nextBtn)
    else :
        nextBtn = browser.find_element(By.XPATH,
                                       f'//*[@id="coveo248b211e"]/div[2]/div[2]/div/div/div/div[3]/div[2]/div[9]/ul/li[12]')
        browser.execute_script("arguments[0].click();", nextBtn)
    sleep(3)

sleep(4)
browser.quit()
