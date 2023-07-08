import csv
from bs4 import BeautifulSoup
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import MyClasses

contents = []
page_num = 0


def getdata(url):
    global page_num
    browser = webdriver.Chrome()
    browser.maximize_window()
    browser.get(url)
    sleep(5)
    searchBtn = browser.find_element(By.XPATH,
                                     "/html/body/div[1]/div[2]/div[5]/div[3]/div/div/div/form/div[4]/div/input[1]")
    searchBtn.click()
    page_num = int(input("Nhập giá trị page : "))
    old = ""
    while page_num < 1706:
        contents = []
        sleep(3)
        soup = BeautifulSoup(browser.page_source, 'lxml')
        print(old)
        if old != "" :
            while old == soup.find("li",class_="navigatorLabel results-display-text text-right").text.strip() :
                sleep(5)
                soup = BeautifulSoup(browser.page_source, 'lxml')

        table = soup.find("table", class_="table table-view LINE")
        if table:
            tbody = table.find("tbody")
            rows = tbody.select("tr")
            for row in rows:
                try:
                    ID = row.get("id")
                    Linktopattern = "http://wipopublish.ipvietnam.gov.vn/wopublish-search/public/detail/patents?id=" + ID
                except:
                    Linktopattern = "N/A"
                cells = row.find_all("div", class_="row")
                try:
                    status = cells[1].find("span").text.strip()
                except:
                    status = "N/A"
                try:
                    name = cells[2].find("span", class_="rs-TITL").text.strip()
                except:
                    name = "N/A"
                try:
                    num_first = cells[3].find("span", class_="rs-AFNB_ORI").text.strip()
                except:
                    num_first = "N/A"
                try:
                    date_apply = cells[3].find("span", class_="rs-AFDT").text.strip()
                except:
                    date_apply = "N/A"
                try:
                    num_announce = cells[4].find("span", class_="rs-GZNB").text.strip() + "\n" + cells[4].find("span",
                                                                                                               class_="rs-PBNB").text.strip()
                except:
                    num_announce = "N/A"
                try:
                    date_announce = cells[4].find("span", class_="rs-PBDT").text.strip()
                except:
                    date_announce = "N/A"
                try:
                    Code_country = cells[6]
                    Code_country = MyClasses.kt_rong(Code_country.text.strip())
                except:
                    Code_country = "N/A"
                try:
                    IPC_type = cells[5].find("span", class_="rs-IPC_ORI")
                    if IPC_type is not None:
                        IPC_type = IPC_type.text.strip()
                except:
                    IPC_type = "N/A"
                try:
                    Num_pattern = cells[7].find("span", class_="rs-RENB").text.strip()
                except:
                    Num_pattern = "N/A"
                try:
                    date_release_pattern = cells[7].find("span", class_="rs-REDT").text.strip()
                except:
                    date_release_pattern = "N/A"
                try:
                    owner_pattern = cells[8].find("span", class_="rs-APNA").text.strip()
                except:
                    owner_pattern = "N/A"
                try:
                    author = cells[8].find("span", class_="rs-INNA").text.strip()
                except:
                    author = "N/A"
                try:
                    summary = cells[9].find("span", class_="rs-ABST").text.strip()
                except:
                    summary = "N/A"
                contents.append((Linktopattern, status, name, num_first, date_apply, num_announce, date_announce,Code_country, IPC_type, Num_pattern, date_release_pattern, owner_pattern, author,summary))
        title_ = ""
        MyClasses.save_to_csv(contents, "800.128", title_)
        page_num = page_num + 1
        print(f"Reading in page : {page_num}")
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
        except:
            browser.execute_script("arguments[0].click();", next_page_btn)


url = "http://wipopublish.ipvietnam.gov.vn/wopublish-search/public/patents?3&query=*:*"
title = (
    "link", "status", "name", "num_first", "date_apply", "num_announce", "date_announce", "Code_country", "IPC_type",
    "Num_pattern", "date_release_pattern", "owner_pattern", "author", "summary")
getdata(url)
