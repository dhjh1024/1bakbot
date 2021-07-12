from selenium import webdriver
from datetime import date
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import time
import telegram

# Telegram Setting
chat = telegram.Bot(token = "1802361644:AAENu52Ui1cqgSMXvtiHkCS2qwzTl1hYTRI")
chat_id = "-1001512203758"
#chat_id = "1510104965"
# text = "abcd"
# chat.sendMessage(chat_id = chat_id, text=text)
# quit()

# webdriver chrome 옵션
options = webdriver.ChromeOptions()
options.add_argument('headless')        # 웹 브라우저를 띄우지 않는 headless chrome 옵션
options.add_argument('disable-gpu')     # GPU 사용 안함
options.add_argument('lang=ko_KR')      # 언어 설정
#options.add_experimental_option('excludeSwitches', ['enable-logging'])  # 로그 숨김

driver = webdriver.Chrome("./chromedriver", options=options)

t = ['월', '화', '수', '목', '금', '토', '일']

#### 네이버예약 ####
dicCamp = {'481805':'돌고래', '14972':'마리원', '163771':'아라뜰', '164989':'물왕숲', '278756':'대부도비치', '59772':'아버지의숲', '160759':'마장호수휴'}
#dicCamp = {'19384':'힐링별밤'}

# 주말 체크
chkday = date.today()
fridays = []
sundays = []
weekNo = 0
while True:
    if chkday.weekday() == 5:
        fridays.append(str(chkday))
        sundays.append(str(chkday + timedelta(days=1)))
        weekNo+=1
        if weekNo == 12:
            break
    chkday = chkday + timedelta(days=1)

#driver.get("https://m.booking.naver.com/booking/3/bizes/481805/items?startDate=2021-07-30&endDate=2021-08-01")
driver.implicitly_wait(3)
# try:
#     driver.find_element_by_class_name("summary_body")
# except Exception as error:
#     print(error)

# quit()


sites = []
sitelist = ""
string = ""
for k in dicCamp.keys():
    for i in range(0,len(fridays)):
        driver.get("https://m.booking.naver.com/booking/3/bizes/"+ k +"/items?startDate=" + fridays[i] + "&endDate=" + sundays[i])

        try:
            find = driver.find_element_by_class_name("result_txt")
            #print(find)
            result = "X"
        except Exception as error:
            #print(error)
            result = "O"
            finds = driver.find_elements_by_css_selector(".summary_body .desc_title")
            for j in finds:
                if j.text == "카라반 CARAVAN" or j.text == "캠프렛 CAMPLET" or j.text == "차박&루프탑&파쇄석 존":       # 물왕숲 제외 SITE
                    continue
                elif k == '278756' and (j.text.find("캠핑 B") > -1 or j.text.find("캠핑 C") > -1 or j.text.find("캠핑 D") > -1):     # 대부도비치 제외 SITE
                    continue
                elif j.text.find("펜션") > -1 or j.text.find("캠핑카") > -1 or j.text.find("방가로") > -1 or j.text.find("커플") > -1:
                    continue
                else:
                    sites.append(j.text.replace("(2박 우선예약)", ""))

            if len(sites) == 0:
                sitelist = ""
                result = "X"
            elif len(sites) >= 1 and len(sites) <=5:
                sitelist = str(sites)
            elif len(sites) > 5:
                sitelist = "예약가능 사이트수 : " + str(len(sites)) + "건"

        print(dicCamp[k] + " / " + fridays[i] + " ~ " + sundays[i] + " : " + result + (" - " if len(sites) > 0 else "") + sitelist)
        if result == "O":
            string += dicCamp[k] + " / " + fridays[i] + " ~ " + sundays[i] + "\n " + sitelist + "\n" + "https://m.booking.naver.com/booking/3/bizes/"+ k +"/items?startDate=" + fridays[i] + "&endDate=" + sundays[i] +"\n"

        sites = []
        sitelist = ""
    if string != "":
        if int(time.strftime('%H')) == 0 or int(time.strftime('%H')) >= 6:   # 새벽시간 알림 차단
            chat.sendMessage(chat_id = chat_id, text=string)
        string = ""


#### 장호비치 ####
string = "장호비치\n"
url = "https://forest.maketicket.co.kr/ticket/GD41"
ableCnt = 0
driver.get(url)
driver.switch_to.window(driver.window_handles[0])

# 이번달
rMonth = driver.find_element_by_css_selector("caption").text
rDate = datetime.strptime(rMonth+".01", "%Y. %m.%d")
days = driver.find_elements_by_css_selector("td[id^=calendar]>strong")
finds = driver.find_elements_by_css_selector(".s3 span")
for i in range(0, len(days)):
    if finds[i].text != "0":
        ableCnt+=1
        rDate = rDate.replace(day = int(days[i].text))
        day = rDate.weekday()
        print(rDate.strftime("%m-%d") + "(" + t[day] + ") : 오토캠핑 " + finds[i].text + "개")
        string += rDate.strftime("%m-%d") + "(" + t[day] + ") : 오토캠핑 " + finds[i].text + "개\n"

# 다음달
driver.find_element_by_css_selector(".nextmonth").click()
time.sleep(1)
rMonth = driver.find_element_by_css_selector("caption").text
rDate = datetime.strptime(rMonth+".01", "%Y. %m.%d")
days = driver.find_elements_by_css_selector("td[id^=calendar]>strong")
finds = driver.find_elements_by_css_selector(".s3 span")
for i in range(0, len(days)):
    if finds[i].text != "0":
        ableCnt+=1
        rDate = rDate.replace(day = int(days[i].text))
        day = rDate.weekday()
        print(rDate.strftime("%m-%d") + "(" + t[day] + ") : 오토캠핑 " + finds[i].text + "개")
        string += rDate.strftime("%m-%d") + "(" + t[day] + ") : 오토캠핑 " + finds[i].text + "개\n"

string += url
if ableCnt > 0:
    chat.sendMessage(chat_id = chat_id, text=string)

'''
#### 캠프운악 ####
# string = "캠프운악\n"
# url = "https://www.campunak.co.kr/Reservation2/Reservation_Site.aspx?sdate=2021-07-02"
# ableCnt = 0
# driver.get("https://www.campunak.co.kr/login.aspx")
# #a = driver.find_element_by_class_name("checkin_table")
# driver.find_element_by_id("ContentMain_txtUserID").send_keys("baezzaes@naver.com")
# driver.find_element_by_id("ContentMain_txtUserPW").send_keys("bjs0321")
# driver.find_element_by_id("ContentMain_btnMemberLogin").click()
# driver.get(url)
# driver.find_element_by_id("ContentMain_btnSearch").click()
# time.sleep(1)
# sites = driver.find_elements_by_css_selector(".site_choice .payamount")
# ables = driver.find_elements_by_css_selector(".site_choice .none")
# for i in range(0, len(sites)):
#     print(sites[i].text + " | " + ables[i].text)
'''

driver.quit()
