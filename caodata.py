import requests
import csv
from bs4 import BeautifulSoup
from MyClasses import courtofappeal

url = "https://www.courtofappeal.org.bs/judgments.php"
content = []
links = []
for i in range(0, 256):
    links.append(f"https://www.courtofappeal.org.bs/judgments.php?skip={i*15}")
headers = {
"Authority": "www.barbadoslawcourts.gov.bb",
"Method": "GET",
"Path": "/case-search-results/?asId=as0",
"Schem": "https",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"vi-VN,vi;q=0.9,fr-FR;q=0.8,fr;q=0.7,en-US;q=0.6,en;q=0.5",
"Cache-Control":"max-age=0",
"Cookie":"PHPSESSID=f0056e3f7626249dddcb34838e75a094; __utma=241215632.383112804.1687928144.1687928144.1687928144.1; __utmc=241215632; __utmz=241215632.1687928144.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1; __utmb=241215632.7.10.1687928144",
"Referer":"https://www.barbadoslawcourts.gov.bb/judgments/",
"Sec-Ch-Ua-Mobile":"?0",
"Sec-Ch-Ua-Platform":"Windows",
"Sec-Fetch-Dest":"document",
"Sec-Fetch-Mode":"navigate",
"Sec-Fetch-Site":"none",
"Sec-Fetch-User":"?1",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}
def getLinkPdf(url):
    r = requests.get(url,headers=headers)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        table = soup.find("table", class_="datatable")
        for row in table.select("tr"):
            if row.find_all("a"):
                href = row.find_all("a")
                for anchor in href:
                    LinkPDF = "https://www.courtofappeal.org.bs/" + anchor.get('href')
    return LinkPDF
def getname(code) :
    html_code = code.prettify()
    start_index = html_code.find('</div>') + len('</div>')
    end_index = html_code.find('<li>', start_index)
    extracted_string = html_code[start_index:end_index].strip()
    return extracted_string
def get_links(urls):
    response = requests.get(urls,headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find("table", class_="datatable")
    for row in table.select("tr"):
        cells = row.find_all("td")
        try:
            fileName = cells[0].text.strip()
            Judgment = cells[1].text.strip()
            Date = cells[2].text.strip()
            JudgementLink = cells[1].select('a')
            for anchor in JudgementLink:
                href = "https://www.courtofappeal.org.bs/" + anchor.get('href')
                content.append(courtofappeal(fileName,Judgment,Date,href,getLinkPdf(href)))
        except:
            print("No Values")
    file_name = "500.118.csv"
    # Ghi dữ liệu vào file CSV
    with open(file_name, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["File Name", "Judgment", "Date", "Link","Link PDF"])
        for obj in content:
            writer.writerow([obj.fileName, obj.Judgment, obj.Date, obj.Link , obj.LinkPDF])
    print("DONE")
for link in links:
    print(link)
    get_links(link)
