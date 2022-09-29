from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import re
import time
import requests
from tkinter import *
from tkinter import ttk
import tkinter as tk
import pandas as pd


# 전국 지역 이름 파싱
def get_place():
    url = 'https://ko.wikipedia.org/wiki/%EB%8C%80%ED%95%9C%EB%AF%BC%EA%B5%AD%EC%9D%98_%EA%B8%B0%EC%B4%88%EC%9E%90%EC%B9%98%EB%8B%A8%EC%B2%B4_%EB%AA%A9%EB%A1%9D'
    response = requests.get(url)
    html = response.text
    place_soup = BeautifulSoup(html, 'html.parser')

    place_s = place_soup.select('div.mw-parser-output > table > tbody > tr > td > a')

    count = 0
    for p in place_s:
        p = str(p)
        place_s[count] = p.split('<')[1].split('>')[1]
        count += 1
    return place_s


# 입력된 해시태그에 맞춰 검색
def insta_searching(word):
    url = "https://www.instagram.com/explore/tags/" + str(word)
    return url

# 첫번재 게시물 클릭
def select_first(driver):
    first = driver.find_element(By.CSS_SELECTOR,"div._aagw")
    first.click()
    time.sleep(5)

# 게시물에서 정보 얻어오기
def get_content(driver):
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    # 본문 내용
    try:
        content = soup.select('div._a9zs')[0].text
        if content.find('나이트') != -1:
            content = 'spam'
    except:
        content = ' '

    # 해시태그
    tags = re.findall(r'#[^\s#,\\]+', content)
    # 본문
    content_filter = content.split("#")[0]
    # 위치
    try:
        place = soup.select('div._aaqm')[0].text
    except:
        place = ' '
    # 이미지 URL
    try:
        img_url = driver.find_elements(By.CLASS_NAME, "_aagv")[-1].find_element(By.CSS_SELECTOR, 'img').get_attribute('src')
    except:
        img_url = ''
    print('URL :' + img_url)
    print('장소 : '+ place)
    print('본문 : ' + content_filter,tags)

    data = [img_url, place, content_filter, tags]
    print(data)
    return data

# 다음 게시물 넘어가기
def move_next(driver):
    try:
        driver.find_element(By.CSS_SELECTOR,"div._aaqg._aaqh > button").click()
        time.sleep(3)
    except:
        return 'none'

def parse_start(id, pw, hashtag):
    # 크롬 브라우저 열기
    driver = webdriver.Chrome('chromedriver.exe')

    driver.get('https://www.instagram.com')
    time.sleep(3)

    # 인스타그램 로그인을 위한 계정 정보
    insta_id = id
    input_id = driver.find_element(By.CSS_SELECTOR, '#loginForm > div > div:nth-child(1) > div > label > input')
    input_id.clear()
    input_id.send_keys(insta_id)

    password = pw
    input_pw = driver.find_element(By.CSS_SELECTOR,
                                   '#loginForm > div.qF0y9.Igw0E.IwRSH.eGOV_.acqo5._4EzTm.kEKum > div:nth-child(2) > div > label > input')

    input_pw.clear()
    input_pw.send_keys(password)
    input_pw.submit()

    time.sleep(5)

    # 게시물을 조회할 검색 키워드 입력 요청
    place_zip = get_place()
    for pl in place_zip:
        word = pl + hashtag
        url = insta_searching(word)
        parsing(driver, url, pl)



def parsing(driver,url,pl):
    # 검색 결과 페이지 열기
    driver.get(url)
    time.sleep(4)  # 코드 수행 시간

    # 첫 번째 게시물 클릭
    select_first(driver)

    # 본격적으로 데이터 수집 시작
    results = []
    ## 수집할 게시물의 수
    target = 50

    tmp_url = ''
    for i in range(target):
        now_url = driver.current_url
        if now_url == tmp_url:
            continue
        else:

            try:
                data = get_content(driver)
                spam = 'spam' # 필터링 된 경우 추가 안함
                if data[2] != spam:
                    results.append(data)
                move_next(driver)
            except:
                time.sleep(2)
                move_next(driver)
        time.sleep(5)
        tmp_url = now_url
    try:
        output_df = pd.DataFrame(results)
        output_df.columns = ['이미지URL', '장소','본문','해시태그']
        output_df.to_excel(pl+'_크롤링.xlsx')
        print(pl+"->크롤링 완료")
    except:
        print("저장된 내용 없음")



id = ""
pw = ""
hashtag="가볼만한곳"

parse_start(id,pw,hashtag)
