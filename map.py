# 본 예제는 Python에서 주소좌표변환 api를 호출하는 예제입니다.
import os
import sys
import urllib.request

from xml.etree import ElementTree
import webbrowser
import folium
global x ,y



def show_map(loc):

    client_id = "rQoDB8wRvqVKhJT6LwAz"
    client_secret = "FBRplP9uiA"
    encText = urllib.parse.quote(loc)
    #url = "https://openapi.naver.com/v1/map/geocode?query=" + encText # json 결과
    url = "https://openapi.naver.com/v1/map/geocode.xml?query=" + encText # xml 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()


    if(rescode==200):
        response_body = response.read()
       # print(response_body.decode('utf-8'))
        tree = ElementTree.fromstring(response_body)
        itemElements = tree.getiterator("point")

        for item in itemElements:
            global x,y
            x = item.find("x")
            y = item.find("y")
    else:
        print("Error Code:" + rescode)



    posx = float(x.text)
    posy = float(y.text)


    # 위도 경도 지정
    map_osm = folium.Map(location=[posy, posx], zoom_start=17)
    # 마커 지정
    folium.Marker([posy, posx], popup='Mt. Hood Meadows').add_to(map_osm)
    # html 파일로 저장
    map_osm.save('osm.html')
    # 지도 열기
    webbrowser.open('osm.html')
