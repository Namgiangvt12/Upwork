import requests
import csv
from bs4 import BeautifulSoup
from MyClasses import LinkPDF

links = []
content = []
for i in range(1, 256):
    links.append(f"https://www.centralbankbahamas.com/bank-supervision/warning-notices?page={i*15}")

def get_links(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table_xpath = "/html/body/div[5]/section[2]/div/div/div[2]/div[2]/div/div[2]/div/div/div[2]/table/tbody"
    table = soup.find("tbody")
    for row in table.find_all("tr"):
        # Lấy dữ liệu từ các ô trong dòng
        cells = row.find_all("td")
        document_title = cells[1].text.strip()
        date_issued = cells[2].text.strip()
        links = cells[1].find("a")["href"]

        # In ra dữ liệu
        content.append(LinkPDF(document_title, date_issued, links))
    print("Done")
    file_name = "400.491.csv"
    # Ghi dữ liệu vào file CSV
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Title", "URL", "Link"])
        for obj in content:
            writer.writerow([obj.tittle, obj.URL, obj.Date])
for link in links:
    get_links(link)
