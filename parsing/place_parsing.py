from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time
import re
import time
import requests
import pandas as pd


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
        list = ['부업', '재테크', '출금', '공짜', '수익', '카톡', '원금', '할인', '부자', 'Repost', '구매', '나이트', '클럽',
                '태풍', '사고', '글귀', '숙제', '과제', '책', '가방']
        for i in list:
            if content.find(i) != -1:
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
        time.sleep(5)
    except:
        return 'none'

def parse_start(id, pw, hashtag_list):
    # 크롬 브라우저 열기
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(executable_path="/usr/lib/chromium-browser/chromedriver", options=chrome_options)
    driver.get('https://www.instagram.com')
    time.sleep(5)

    # 인스타그램 로그인을 위한 계정 정보
    insta_id = id
    input_id = driver.find_element(By.CSS_SELECTOR, '#loginForm > div > div:nth-child(1) > div > label > input')
    input_id.clear()
    input_id.send_keys(insta_id)

    password = pw
    input_pw = driver.find_element(By.CSS_SELECTOR, ' #loginForm > div > div:nth-child(2) > div > label > input')

    input_pw.clear()
    input_pw.send_keys(password)
    input_pw.submit()

    time.sleep(5)

    # 게시물을 조회할 검색 키워드 입력 요청
    for hashtag in hashtag_list:
        word = hashtag
        url = insta_searching(word)
        parsing(driver, url, hashtag)



def parsing(driver,url,pl):
    # 검색 결과 페이지 열기
    driver.get(url)
    time.sleep(8)  # 코드 수행 시간

    try:# 첫 번째 게시물 클릭
        select_first(driver)

        # 본격적으로 데이터 수집 시작
        results = []
        ## 수집할 게시물의 수
        target = 100

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
    except:
        pass


# 인스타그램 아이디, 비번, 해시태그 입력하는곳
id = "parsingtag3"
pw = "zoqtmxhs"

hashtag_list = ['캠핑', '캠퍼','캠핑장추천','디저트','액티비티','액티비티추천','경비행기','패러글라이딩','체험','스카이워크','요트','루지','양궁','사격','전통체험','체험농장','문화유산','왕실문화','유물','역사','문화재청','미술관',
                '박물관','전시','전시회','먹방로드','먹스타그램','공방','커플여행,','우정여행','가족여행']

parse_start(id,pw,hashtag_list)

