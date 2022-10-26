import pandas as pd
from pandas import Series, DataFrame
import numpy as np

df = pd.read_excel('가평_크롤링.xlsx', engine = "openpyxl")
arr = np.array(df)
test_list = np.delete(arr, 0, axis = 1)
#test_list = [['장소','본문','태그','img_url'],['장소2','본문2','태그2','img_url2'],['장소3','본문3','태그3','img_url3'],] #입력리스트 ex) 엑셀 데이터
label_output = [] #출력리스트
theme = 9 #테마 개수

list_count = len(test_list)

def labeling(url,place,main,tags):
    print('이미지출력 : '+ url)
    print('장소 : '+ place)
    print('본문 : '+ main)
    print('태그 : '+ tags)   
    sel = input("라벨링 해주세요 1.가볼만한곳 2.가족여행 3.우정여행 4.전통 5.체험 6.캠핑 7.관람 8.맛집 9.카페 \n")
    sel_list = ['1' if l+1 == int(sel) else '0' for l in range(theme)]   
    label_output.append([place,main,tags,sel_list])
    
for i in range(list_count):
    labeling(str(test_list[i][0]),str(test_list[i][1]),str(test_list[i][2]),str(test_list[i][3]))

print(label_output)

label_df = pd.DataFrame(label_output)
label_df.columns = ['장소','본문','태그','가볼만한곳']
label_df.to_excel('가평_크롤링_v2.xlsx')