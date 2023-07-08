import csv
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from MyClasses import save_to_csv,kt_rong

contents = []
page_num = 0


def getdata(url):
    global page_num
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(url)
    sleep(5)
    searchBtn = browser.find_element(By.XPATH,
                                     "/html/body/div[1]/div[5]/div[3]/div[2]/div/div[1]/div[2]/div/div/span/span/span/span[4]/span/a/span[1]")
    searchBtn.click()
    page_num = int(input("Nhập giá trị page : "))
    old = ""
    while page_num < 2981:
        contents = []
        sleep(3)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        if old != "" :
            while old == soup.find("li",class_="navigatorLabel results-display-text text-right").text.strip() :
                sleep(5)
                soup = BeautifulSoup(browser.page_source, 'lxml')
        table = soup.find("table",class_="table table-view COLUMN")
        old = soup.find("li", class_="navigatorLabel results-display-text text-right").text.strip()
        print(old)
        tbody = table.find("tbody")
        rows = tbody.select("tr")
        for row in rows :
            cells = row.select("td")
            mID = row.get("id")
            Link_trademark = "https://online.dip.gov.la/wopublish-search/public/detail/patents?id=" + mID
            t_href = cells[1].find("img",class_="rs-DRAWING img-responsive column-img" )
            if t_href is not None  and t_href.get("src") != "/wopublish-resources/img/blank.png" :
                Link_logo =  "https://online.dip.gov.la/" + t_href.get("src")
            else: Link_logo = "N/A"
            Name = kt_rong(cells[2].text.strip())
            Document_number = kt_rong(cells[3].text.strip())
            Registration_number = kt_rong(cells[4].text.strip())
            Day_of_submission = kt_rong(cells[5].text.strip())
            Expiration_date = kt_rong(cells[6].text.strip())
            Date_of_registration = kt_rong(cells[7].text.strip())
            NICE_classification = kt_rong(cells[8].text.strip())
            The_petitioner = kt_rong(cells[9].text.strip())
            Representative_Company = kt_rong(cells[10].text.strip())
            Types_of_sub_claims = kt_rong(cells[11].text.strip())
            Status = kt_rong(cells[12].text.strip())
            contents.append((Link_trademark,Link_logo,Name, Document_number, Registration_number, Day_of_submission,
                             Date_of_registration,Expiration_date, NICE_classification ,
                             The_petitioner, Representative_Company, Types_of_sub_claims, Status))


        save_to_csv(contents, "800.133", title)
        page_num = page_num + 1
        print(f"Readed in page : {page_num}")
        file_name = f"process.txt"
        with open(file_name, mode='w', newline='', encoding="utf-8") as file:
            file.write(str(page_num))
        wait = WebDriverWait(browser, 200)
        wait.until(EC.invisibility_of_element_located((By.ID, "loadingDiv")))
        old = soup.find("li", class_="navigatorLabel results-display-text text-right").text.strip()
        next_page_btn = browser.find_element(By.XPATH,
                                             "//i[contains(@class, 'fa-step-forward') and contains(@class, 'fa-lg') and contains(@class, 'pageNumber')]")
        try:
            next_page_btn.click()
        except :
            browser.execute_script("arguments[0].click();", next_page_btn)

    browser.quit()
url = "https://online.dip.gov.la/wopublish-search/public/trademarks?0&query=*:*"
title = (
    "Link_trademark","Link_logo","Name", "Document_number", "Registration_number", "Day_of_submission",
                             "Date_of_registration", "","Expiration_date", "NICE_classification" ,
                             "The_petitioner", "Representative_Company", "Types_of_sub_claims", "Status")
getdata(url)

