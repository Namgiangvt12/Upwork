import requests
import csv
from bs4 import BeautifulSoup
from MyClasses import Jugde

url = "https://www.bahamasjudiciary.com/judgments/"
content = []

def getname(code) :
    html_code = code.prettify()
    start_index = html_code.find('</div>')
    start_index = html_code.find('</div>') + len('</div>')
    end_index = html_code.find('<li>', start_index)
    extracted_string = html_code[start_index:end_index].strip()
    return extracted_string
def get_links(urls):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("div", class_="judgements ajax-list")
    for row in table.select("div ul.judgements__row"):
        # Lấy dữ liệu từ các ô trong dòng
        cells = row.find_all("li")
        JUDGMENT = cells[0].text.strip().replace("JUDGMENT","")
        DATE = cells[2].text.strip().replace("DATE","")
        LINKPDF = cells[3].select('a')
        for anchor in LINKPDF:
            href = anchor.get('href')
            content.append(Jugde(JUDGMENT, getname(cells[1]), DATE,href))

    file_name = "500.117.csv"
    # Ghi dữ liệu vào file CSV
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["JUDGMENT","JUDGE","DATE","href"])
        for obj in content:
            writer.writerow([obj.JUDGMENT, obj.JUDGE, obj.DATE,obj.LINKPDF])
    print("DONE")

get_links(url)
