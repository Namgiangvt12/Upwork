import time

import requests

from MyClasses import kt_rong,save_to_csv
from bs4 import BeautifulSoup
import pandas as pd
url = "https://www.unofficialroyalty.com/current-monarchies/thai-royals/thai-royal-family-2/"
contents = []
header = {
"Authority":"www.ngocentre.org.vn",
"Method":"GET",
"Path" : "/ingodirectory",
"Scheme":"https",
"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
"Accept-Encoding":"gzip, deflate, br",
"Accept-Language":"vi,vi-VN;q=0.9,en-US;q=0.8,en;q=0.7",
"Cache-Control":"max-age=0",
"Cookie":"SESS2616722a74148ebb7216411383223c3d=fpn5onj7eu7n7oo6ube39b2ka5; has_js=1; __utmc=23834021; __utmz=23834021.1688178323.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=23834021.1652650096.1688178323.1688178323.1688180545.2; __utmb=23834021.1.10.1688180545",
"If-Modified-Since":"Sat, 01 Jul 2023 02:42:22 GMT",
"Sec-Ch-Ua": r"Not.A/Brand;v=8, Chromium;v=114, Google Chrome;v=114",
"Sec-Ch-Ua-Mobile":"?0",
"Sec-Ch-Ua-Platform":"Windows",
"Sec-Fetch-Dest":"document",
"Sec-Fetch-Mode":"navigate",
"Sec-Fetch-Site":"none",
"Sec-Fetch-User":"?1",
"Upgrade-Insecure-Requests":"1",
"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
}


def getdata(url_,header_):

    respones = requests.get(url_,headers=header_)
    if respones.status_code == 200 :
        soup = BeautifulSoup(respones.content,'lxml')
        print(soup.text)


getdata(url,header)
#title = ["Name_Organization","Type_Organization",",Main_area_of_expertise","Additional_information"]
#save_to_csv(contents,"1.000.131",title)


