from selenium import webdriver
from time import sleep
from selenium.webdriver.common.by import By
import threading


def doc_file_text(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
    return content


def chuyen_doi_sang_int(text):
    try:
        number = int(text)
        return number
    except ValueError:
        print("Nội dung không thể chuyển đổi thành integer.")


# thiết lập môi trường web
num_browsers = 2
idHuyen = 1
url = f'https://congbobanan.toaan.gov.vn/0tat1cvn/ban-an-quyet-dinh'
fileName = "50.0478_4"
browsers = []
threads = []
lock = threading.Lock()


def getdata(browser, numDoc, page):
    sleep(3)
    id = 0
    for num in range(1, 21):
        tittle = browser.find_element(By.XPATH,
                                      f'/html/body/form/div[4]/section/div[2]/div/div[2]/div[2]/div/div[1]/div/div[{num}]/a')
        finalTittle = tittle.text[:-12]
        href = tittle.get_attribute("href")
        dateCase = browser.find_element(By.XPATH,
                                        f'/html/body/form/div[4]/section/div[2]/div/div[2]/div[2]/div/div[1]/div/div[{num}]/a/h4/span/time')
        date = dateCase.text.replace("(", "")
        date = date.replace(")", "")
        objectSui = browser.find_element(By.XPATH,
                                         f'/html/body/form/div[4]/section/div[2]/div/div[2]/div[2]/div/div[1]/div/div[{num}]/div[1]/div/p/span')
        object = objectSui.text.replace('"', '')
        Judgment_Level = browser.find_element(By.XPATH,
                                              f'/html/body/form/div[4]/section/div[2]/div/div[2]/div[2]/div/div[1]/div/div[{num}]/div[2]/div[1]/span')
        Application_of_precedent = browser.find_element(By.XPATH,
                                                        f'/html/body/form/div[4]/section/div[2]/div/div[2]/div[2]/div/div[1]/div/div[{num}]/div[2]/div[2]/span')
        kindOf = browser.find_element(By.XPATH,
                                      f'/html/body/form/div[4]/section/div[2]/div/div[2]/div[2]/div/div[1]/div/div[{num}]/div[3]/div[1]/span')
        Corrections = browser.find_element(By.XPATH,
                                           f'/html/body/form/div[4]/section/div[2]/div/div[2]/div[2]/div/div[1]/div/div[{num}]/div[3]/div[2]/span')
        infoCase = browser.find_element(By.XPATH,
                                        f'/html/body/form/div[4]/section/div[2]/div/div[2]/div[2]/div/div[1]/div/div[{num}]/p/span')
        infoCase_2 = infoCase.text.replace('"', '')
        id = id + 1
        print(
            f'{id} | {numDoc} | {finalTittle} | {href} | {date} | {object} | {Judgment_Level.text} | {Application_of_precedent.text} | {kindOf.text} | {Corrections.text} | {infoCase_2}')
        file_path = f'{fileName}_{numDoc}.csv'
        with lock:
            with open(file_path, 'a', encoding="utf-8") as csv:
                csv.write(
                    f'\"{finalTittle}\",{href},{date},\"{object}\",{Judgment_Level.text},{Application_of_precedent.text},{kindOf.text},{Corrections.text},\"{infoCase_2}\"\n')
        sleep(1)


def thread_task(url, idHuyen=idHuyen):
    browser = webdriver.Chrome()
    browser.get(url)
    sleep(3)
    submit = browser.find_element(By.XPATH,
                                  f'/html/body/form/div[3]/div/div/div[2]/div[2]/table/tbody/tr[6]/td[2]/input')
    submit.click()
    submit2 = browser.find_element(By.XPATH,
                                   f'/html/body/form/div[3]/div/div/div[2]/div[2]/div/input')
    submit2.click()
    select = browser.find_element(By.XPATH,
                                  f'/html/body/form/div[4]/section/div[2]/div/div[1]/div/div/div/div[3]/div[1]/ul/li/select/option[5]')
    select.click()
    sleep(5)
    activeHuyen = browser.find_element(By.XPATH,
                                       f'/html/body/form/div[4]/section/div[2]/div/div[1]/div/div/div/div[3]/div[2]/ul/li/div')
    activeHuyen.click()
    sleep(2)
    chonTinh = browser.find_element(By.XPATH,
                                    f'/html/body/form/div[4]/section/div[2]/div/div[1]/div/div/div/div[3]/div[2]/ul/li/div/div/ul/li[{idHuyen}]')
    chonTinh.click()
    findBtn = browser.find_element(By.XPATH,
                                   f'/html/body/form/div[4]/section/div[2]/div/div[1]/div/div/div/div[6]/div[3]/ul/li/div/input[1]')
    findBtn.click()
    sleep(10)
    findNumpage = browser.find_element(By.XPATH,
                                       f'/html/body/form/div[4]/section/div[2]/div/div[2]/div[2]/div/div[2]/div[1]/span[2]')
    numPage = int(findNumpage.text) + 1

    try:
        page = chuyen_doi_sang_int(doc_file_text(f"process_{idHuyen}.txt")) + 1
    except:
        page = 1
    for page in range(page, numPage):
        try:
            getdata(browser, idHuyen, page)
            with open(f'process_{idHuyen}.txt', 'w') as file:
                file.write(f"{page}\n")
        except:
            print("nothing to get")
    sleep(20)
    browser.quit()


for _ in range(num_browsers):
    idHuyen += 1
    thread = threading.Thread(target=thread_task, args=(url, idHuyen))
    thread.start()
    threads.append(thread)
for thread in threads:
    thread.join()
