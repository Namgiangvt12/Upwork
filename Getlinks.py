import csv
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor
from MyClasses import barbadoslawcourts


base_url = "https://www.barbadoslawcourts.gov.bb/"
judgment_url = f"{base_url}/case-search-results/?asId=as0"
content = []
headers = {
"Authority": "commerce.gov.bb",
"Method": "GET",
"Path": "/cases/",
"Schem": "https",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
"Cache-Control":"max-age=0",
"Cookie":"cookiesession1=678B28680691A4D7ED0886C8F04CFAAA; _gid=GA1.3.1815715186.1687967454; _ga=GA1.3.337703036.1687967454; _ga_81VSG8ZGDQ=GS1.1.1688006514.3.1.1688007941.0.0.0",
"Host" : "sb.judiciary.gov.ph",
"Sec-Ch-Ua-Mobile":"?0",
"Sec-Ch-Ua-Platform":"Windows",
"Sec-Fetch-Dest":"document",
"Sec-Fetch-Mode":"navigate",
"Sec-Fetch-Site":"none",
"Sec-Fetch-User":"?1",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}


def get_link_pdf(url):
    r = requests.get(url, headers=headers)
    link_pdf =""
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find("table", class_="datatable")
        for row in table.select("tr"):
            if row.find_all("a"):
                href = row.find_all("a")
                for anchor in href:
                    link_pdf = f"{base_url}/{anchor.get('href')}"
    if link_pdf != "" :
        return link_pdf
    else:
        link_pdf = "N/A"
        return link_pdf


def get_name(code):
    html_code = code.prettify()
    start_index = html_code.find('</div>') + len('</div>')
    end_index = html_code.find('<li>', start_index)
    extracted_string = html_code[start_index:end_index].strip()
    return extracted_string

PDFID = 0
content = []
def process_link(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    browser = webdriver.Chrome(options=chrome_options)
    browser.get(url)
    sleep(2)
    try :
        soup = BeautifulSoup(browser.page_source, 'lxml')
        div_elements = soup.find_all('tbody')
        for table in div_elements :
            for row in table.select("tr"):
                cells = row.find_all("td")
                if cells:
                    Title = cells[0].text.strip()
                    date = cells[1].text.strip()
                    href_element = cells[0].find("a")
                    if href_element:
                        href = "https://sb.judiciary.gov.ph/" + href_element.get("href")
                        content.append((Title,date, href.replace("././","")))
    except Exception as e:
        print("An error occurred:", str(e))
    finally:
        browser.quit()
def save_to_csv(data,filename):
    file_name = f"{filename}.csv"
    with open(file_name, mode='w', newline='',encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Title","Date", "Link"])
        for dat in data :
            writer.writerow(dat)
    print("DONE")


def main():
    process_link("https://sb.judiciary.gov.ph/recentdecision.php?docutype=DECISIONS&year=2021&show=Show") #tăng 1
    fileName = "500.437" #giảm 1
    #links = [f"https://commerce.gov.bb/cases/page/{i}/" for i in range(1,9)]
    #with ThreadPoolExecutor(8) as executor:
        #executor.map(process_link, links)
    save_to_csv(content,fileName)

if __name__ == "__main__":
    main()
