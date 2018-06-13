from tkinter import*
#from search import *
from tkinter import font
import tkinter.messagebox
from io import BytesIO
import urllib
import urllib.request
from PIL import Image,ImageTk
from urllib import request
from xml.etree import ElementTree
from mail import *
from map import *
import webbrowser

url_home = 'http://openapi.animal.go.kr/openapi/service/rest/abandonmentPublicSrvc/'
serviceKey = 'serviceKey=OyfS4qqxnYyHXNdGgHg%2Bem2F%2FLAjaG4C0X2kgqycc%2B2G3%2F0flCjg9GIptnv23C3UXWRH3wjd3EuE31%2FGSX71ZA%3D%3D'
url_sido = url_home + "sido?" + serviceKey
url_dog = url_home + "kind?" + serviceKey + "&up_kind_cd=417000"

pgNm = 1

root=Tk()
root.geometry("470x650+500+200")
DataList = []

DataList.append("강아지")

def searchAnimal(e1, e2, e3, e4 , k):
    global sido_code, sigungu_code, bgn_date, end_date, mailData
    menuStatus = True
    
    i = 1
    bgn_date = e3#input("검색시작 날짜(YYYYMMDD): ")
    end_date = e4#input("검색종료 날짜(YYYYMMDD): ")

    sido_name = e1#input("시/도를 입력하세요: ")
    url_sido = url_home + "sido?" + serviceKey
    sido_code = getRegionCode(url_sido, sido_name)

    sigungu_name =e2 #input("시/군/구를 입력하세요: ")
    url_sigungu = url_home + 'sigungu?' + serviceKey + '&upr_cd=' + sido_code
    sigungu_code = getRegionCode(url_sigungu, sigungu_name)

    

   # animal_kind = input("동물 종류를 입력하세요(1.개/ 2.고양이/ 3.기타/ 4.상관없음: ")
    animal_kind = k
    
    if animal_kind == 1: 
        animal_code = "&upkind=417000"
        kind_code = ""

    elif animal_kind == 2: 
        animal_code = "&upkind=422400"
        kind_code = ""
    elif animal_kind == 3:
        animal_code = "&upkind=429900"
        kind_code = ""
    elif animal_kind == 4:
        animal_code = ""
        kind_code = ""
        
    url_searchAbandonment = \
            url_home+'abandonmentPublic?' + serviceKey + '&bgnde=' + bgn_date + '&endde=' + end_date \
            + animal_code + kind_code +'&org_cd=' + sigungu_code + \
            '&pageNo=' + str(pgNm) + '&numOfRows=1'
    response = request.urlopen(url_searchAbandonment).read()
    tree = ElementTree.fromstring(response)
    itemElements = tree.getiterator("item")
    
    for item in itemElements:
        printAnimal(item)
        


def printAnimal(item):
    global mailData, loc, pic
    
    RenderText.insert(INSERT, "-----동물정보-----\n")
    
    processState = item.find("processState")
    kindCd = item.find("kindCd")
    age = item.find("age")
    sexCd = item.find("sexCd")
    colorCd = item.find("colorCd")
    neuterYn = item.find("neuterYn")
    specialMark = item.find("specialMark")
    weight = item.find("weight")
    happenPlace = item.find("happenPlace")
    photo = item.find("popfile")
    
    
    RenderText.insert(INSERT, "상태: "+ processState.text + "\n")
    RenderText.insert(INSERT, "품종: "+ kindCd.text+ "\n")
    RenderText.insert(INSERT, "나이: "+ age.text+ "\n")
    RenderText.insert(INSERT, "성별: "+ sexCd.text+ "\n")
    RenderText.insert(INSERT, "색상: "+ colorCd.text+ "\n")
    RenderText.insert(INSERT, "중성화 여부: "+ neuterYn.text+ "\n")
    RenderText.insert(INSERT, "특징: "+ specialMark.text+ "\n")
    RenderText.insert(INSERT, "체중: "+ weight.text+ "\n")
    RenderText.insert(INSERT, "발견장소: "+ happenPlace.text+ "\n")
    RenderText.insert(INSERT, "사진: "+ photo.text+ "\n")
    RenderText.insert(INSERT, "-----보호 정보-----"+ "\n")
    
    happenDt = item.find("happenDt")
    careNm = item.find("careNm")
    careAddr = item.find("careAddr")
    careTel = item.find("careTel")
    chargeNm = item.find("chargeNm")
    officetel = item.find("officetel")
    orgNm = item.find("orgNm")
    noticeNo = item.find("noticeNo")
    desertionNo = item.find("desertionNo")

    RenderText.insert(INSERT,"접수일: "+ happenDt.text+ "\n")
    RenderText.insert(INSERT,"보호소 이름: "+ careNm.text+ "\n")
    RenderText.insert(INSERT,"보호 주소: "+ careAddr.text+ "\n")
    RenderText.insert(INSERT,"보호소 전화번호: "+ careTel.text+ "\n")
    RenderText.insert(INSERT,"담당자: "+ chargeNm.text+ "\n")
    RenderText.insert(INSERT,"담당자 연락처: "+ officetel.text+ "\n")
    RenderText.insert(INSERT,"관할기관: "+ orgNm.text+ "\n")
    RenderText.insert(INSERT,"공고번호: "+ noticeNo.text+ "\n")
    RenderText.insert(INSERT,"페이지번호 : ")
    RenderText.insert(INSERT,pgNm)

    mailData = "-----동물정보-----" +"\n상태: "+processState.text +"\n품종: " + kindCd.text +"\n나이: "+ \
               age.text+"\n성별: "+ sexCd.text +"\n색상: "+ colorCd.text +"\n중성화 여부: "+ neuterYn.text +\
               "\n특징: "+ specialMark.text +"\n체중: "+ weight.text +"\n발견장소: "+ happenPlace.text \
               +"\n사진: "+ photo.text + "\n-----보호 정보-----"+"\n접수일: "+ happenDt.text + "\n보호소 이름: " + \
               careNm.text + "\n보호 주소: "+ careAddr.text + "\n보호소 전화번호: "+ careTel.text + "\n담당자: "+ \
               chargeNm.text + "\n담당자 연락처: " + officetel.text + "\n관할기관: "+ orgNm.text + "\n공고번호: "+ \
               noticeNo.text + "\n유기번호: "+ desertionNo.text

    loc = careAddr.text
    pic = photo.text
   

 

def getRegionCode(url, search_name):
    response = request.urlopen(url).read()
    tree = ElementTree.fromstring(response)
    itemElements = tree.getiterator("item")
    for item in itemElements:
        name = item.find('orgdownNm')
        name = name.text
        if name == search_name:
            result = item.find("orgCd")
            return result.text

def getDogKindCode(search_name):
    response = request.urlopen(url_dog).read()
    tree = ElementTree.fromstring(response)
    itemElements = tree.getiterator("item")
    for item in itemElements:
        name = item.find('KNm')
        name = name.text
        if name == search_name:
            result = item.find("kindCd")
            return str(result.text)

def printItem(url, item_name):
    response = request.urlopen(url).read()
    tree = ElementTree.fromstring(response)
    itemElements = tree.getiterator("item")
    for item in itemElements:
        name = item.find(item_name)
        print(name.text)
        
def SearchButtonAction():#선택을 눌렀을때 해야하는 짓
    global pgNm
    sido = e1.get()
    sigungu = e2.get()
    begin = e3.get()
    end = e4.get() 
    k = slb.curselection()[0] +1
    pgNm = 1
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)  
    searchAnimal(e1.get(), e2.get(), e3.get(), e4.get(), slb.curselection()[0] +1 )
    RenderText.configure(state='disabled')

def nextpage():
    global pgNm
    pgNm +=1
    RenderText.configure(state='normal')
    RenderText.delete(0.0, END)  
    searchAnimal(e1.get(), e2.get(), e3.get(), e4.get(), slb.curselection()[0] +1 )
    RenderText.configure(state='disabled')
def backpage():
    global pgNm
    if paNm > 1:
        pgNm -=1
        RenderText.configure(state='normal')
        RenderText.delete(0.0, END)  
        searchAnimal(e1.get(), e2.get(), e3.get(), e4.get(), slb.curselection()[0] +1 )
        RenderText.configure(state='disabled')

def sendmail():
    global mailData
    if mailData != None:
        sendMail( e5.get() , mailData)
def showmap():
    global loc
    if loc != None:
        show_map(loc)
def showpic():
    global pic
    print(pic)
    webbrowser.open(pic)
    


rtsb = Scrollbar(root)
rtsb.pack()
rtsb.place(x=700,y=250)

TempFont = font.Font(root, size=10, family = 'Consolas')
RenderText = Text(root, width=49, height = 27, borderwidth= 12, relief ='ridge' , yscrollcommand = rtsb.set)
RenderText.pack()
RenderText.place(x=10, y=170)
rtsb.config(command = RenderText.yview)
rtsb.pack(side=RIGHT, fill= BOTH)
RenderText.configure(state='disabled')

def printtest():
    data = e1.get() + e2.get() + e3.get() + e4.get()
    data2 = slb.curselection()[0]
    print(data2)



l1 = Label(root , text="도")
l2 = Label(root , text="시")
l3 = Label(root , text="시작일")
l4 = Label(root , text="종료일")
l1.pack()
l2.pack()
l3.pack()
l4.pack()
l1.place(x=10, y=10)
l2.place(x=250, y=10)
l3.place(x=10, y=40)
l4.place(x=250, y=40)


e1 = Entry(root) #도
e2 = Entry(root) #시
e3 = Entry(root) #시작일
e4 = Entry(root) #종료일
e1.pack()
e2.pack()
e3.pack()
e4.pack()
e1.place(x=50, y=10)
e2.place(x=290, y=10)
e3.place(x=50, y=40)
e4.place(x=290, y=40)


lsb = Scrollbar(root)
#lsb.pack()
#lsb.place( x=500, y=300)

slb = Listbox(root, activestyle='none',width=8, height=4, borderwidth=8, relief='ridge', yscrollcommand=lsb.set)
slb.insert(1,"개")
slb.insert(2,"고양이")
slb.insert(3,"기타")
slb.insert(4,"상관없음")
slb.pack()
slb.place(x=50, y = 70)

button = Button(root, text="검색", command=SearchButtonAction) #정보 입력하면 검색하는 버튼
button.pack()
button.place(x=400, y = 70)

b2 = Button(root, text="이전", command=backpage) #정보 입력하면 검색하는 버튼
b2.pack()
b2.place(x=75, y = 500)

b3 = Button(root, text="다음", command=nextpage) #정보 입력하면 검색하는 버튼
b3.pack()
b3.place(x=275, y = 500)



b4 = Button(root, text="메일전송", command=sendmail) #정보 입력하면 검색하는 버튼
b4.pack()
b4.place(x=180, y = 550)

b5 = Button(root, text="사진보기", command=showpic) #정보 입력하면 검색하는 버튼
b5.pack()
b5.place(x=25, y = 600)

b6 = Button(root, text="지도보기", command= showmap) #정보 입력하면 검색하는 버튼
b6.pack()
b6.place(x=125, y = 600)

e5 = Entry(root) #종료일
e5.pack()
e5.place(x=10, y=550)


root.mainloop()






