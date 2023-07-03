from selenium import webdriver
from time import sleep
import csv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser = webdriver.Chrome()
url = f'https://www.canada.ca/en/financial-consumer-agency/services/industry/commissioner-decisions/archived-decisions.html'
browser.get(url)
wait = WebDriverWait(browser, 10)
sleep(3)
elements = wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '.mwsbodytext.text.parbase.section')))
sect = 3
for element in elements:
    for num in range(1, 16):
        decisionName = browser.find_element(By.XPATH, f'/html/body/main/div[{sect}]/p[{num}]')
        try :
            decisionLink = browser.find_element(By.XPATH, f'/html/body/main/div[{sect}]/p[{num}]/strong/a')
            decisionHref = decisionLink.get_attribute("href")
        except:
            decisionHref = "None"

        contentDecisions = element.find_elements(By.XPATH, f'/html/body/main/div[{sect}]/ul[{num}]')
        for contentDecision in contentDecisions:
            date_decision = contentDecision.find_element(By.XPATH, f'/html/body/main/div[{sect}]/ul[{num}]/li[1]')
            content = contentDecision.find_element(By.XPATH, f'/html/body/main/div[{sect}]/ul[{num}]/li[2]')
            finalDate = date_decision.text.replace("Posted on ","")
            print(f"{decisionName.text},{decisionHref},\"{finalDate}\",\"{content.text}\"")
            file_path = '40.0088_10.csv'
            with open(file_path, 'a') as file:
                file.write(f"{decisionName.text},{decisionHref},\"{finalDate}\",\"{content.text}\"\n")
    sect = sect + 1
    if sect == 7 :
        for num in range(1, 26):
            decisionName = browser.find_element(By.XPATH, f'/html/body/main/div[{sect}]/p[{num}]')
            try:
                decisionLink = browser.find_element(By.XPATH, f'/html/body/main/div[{sect}]/p[{num}]/strong/a')
                decisionHref = decisionLink.get_attribute("href")
            except:
                decisionHref = "None"

            contentDecisions = element.find_elements(By.XPATH, f'/html/body/main/div[{sect}]/ul[{num}]')
            for contentDecision in contentDecisions:
                date_decision = contentDecision.find_element(By.XPATH, f'/html/body/main/div[{sect}]/ul[{num}]/li[1]')
                content = contentDecision.find_element(By.XPATH, f'/html/body/main/div[{sect}]/ul[{num}]/li[2]')
                finalDate = date_decision.text.replace("Posted on ", "")
                print(f"{decisionName.text},{decisionHref},\"{finalDate}\",\"{content.text}\"")
                file_path = '40.0088_10.csv.csv'
                with open(file_path, 'a') as file:
                    file.write(f"{decisionName.text},{decisionHref},\"{finalDate}\",\"{content.text}\"\n")


browser.quit()