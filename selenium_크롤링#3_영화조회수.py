from selenium import webdriver
import time
import requests
from fake_useragent import UserAgent
import datetime

options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])

now = datetime.datetime.now()
nowDatetime = now.strftime('%Y-%m-%d_%H-%M-%S')
genres = ["kmovie","engmovie","oldmovie","animovie"]  # k:한국 eng:서양 old:고전 ani:애니
file_name = str(nowDatetime) + ".csv"
f = open(file_name, "w")
#ua = UserAgent()
#ua.random
#headers = {'UserAgent' : ua}
#headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36'}
res = webdriver.Chrome("C:\\Users\\WIN10X64\\desktops\\비둘기\\web\\chromedriver.exe", options=options)

firstpage = 1
lastpages = {"kmovie":39, "engmovie":169, "oldmovie":164, "animovie":34 }
#"kmovie":39,"engmovie":169,"oldmovie"=164,"animovie"=34
f.write("No.,장르,댓글수,조회수,이름" + "\n" )
for genre in genres:
    print(" --%s 장르로 변경 중 --" %genre)
    lastpage = lastpages[genre]
    print(" --" + genre + " 1/%s 페이지 작업 중--" %lastpage)
    Base_url = "https://b11.koreanz.fun/bbs/board.php?bo_table=" + genre + "&page="
    url= Base_url + str(firstpage)
    res.get(url)
    time.sleep(1)

    no = 1
    titles = [] #리스트 초기화
    views = [] #리스트 초기화
    lists = [] #리스트 초기화
    #sites = requests.get(url, headers = headers)
    lists = res.find_elements_by_class_name("list-row")
    print(len(lists))
    for currentpage in range(firstpage, lastpage+1):
        if currentpage == 1:
            pass
        else:
            url= Base_url + str(currentpage)
            print(" --" + genre +" " + str(currentpage) + "/%s 페이지 작업 중--" %lastpage)
            res.get(url)
            time.sleep(1)
            lists = res.find_elements_by_class_name("list-row")
        print(str(currentpage))
        for i in range(len(lists)):  
            try:
                country = lists[i].find_element_by_class_name("div-title-underline-thin")
                title = lists[i].find_element_by_class_name("list-desc")
                title_text = title.text
                title_text = title_text.replace(",","(")
                view = lists[i].find_element_by_class_name("pull-right")
                print(str(no) + "  " + genre + "  " + view.text +"  "+ title_text)
                f.write(str(no) + "," + genre + "," + view.text + ", ," + title_text + "\n" )
                no = no + 1
            except:
                pass
        print(" --"+genre + " " + str(currentpage)+"/%s 페이지 작업완료" %lastpage)
        currentpage = currentpage + 1
print(" --모든 작업이 끝났습니다. %s 파일을 확인하세요" %file_name)
f.close()