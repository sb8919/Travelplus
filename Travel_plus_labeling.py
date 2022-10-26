import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
import tkinter
from IPython.display import clear_output
from tkinter import messagebox

# 데이터 파일 이름
file_name = '강북_크롤링'

df = pd.read_excel(file_name+'.xlsx', engine = "openpyxl")
arr = np.array(df)
test_list = np.delete(arr, 0, axis = 1)
#test_list = [['장소','본문','태그','img_url'],['장소2','본문2','태그2','img_url2'],['장소3','본문3','태그3','img_url3'],] #입력리스트 ex) 엑셀 데이터
label_output = [] #출력리스트
theme = 9 #테마 개수(스팸 포함)

list_count = len(test_list) # 리스트 개수

def finsih_alram():
    print('----------------------------------------------------\n\n\t\t\t라벨링완료\n\n----------------------------------------------------')
    # tkinter.messagebox.showinfo('라벨링완료', '라벨링이완료되었습니다.')
    
def labeling(url,place,main,tags):
    try:
        image = io.imread(url)
        plt.imshow(image)
        plt.show()
    except:
        print('이미지출력 : 안됨')
    print('장소 : '+ place)
    print('본문 : '+ main)
    print('태그 : '+ tags)   
    sel = input("\n라벨링 해주세요 1.가볼만한곳 2.가족여행 3.우정여행 4.전통 5.체험 6.캠핑 7.관람 8.맛집 9.카페 0.스팸 \n")
    if sel == '0':# 스팸일때 게시물 Pass
        return
    else:
        sel_list = ['1' if l+1 == int(sel) else '0' for l in range(theme)]   
    
        content_output_list = [tags,main,place] # 엑셀에 추가할 목록
        for c in content_output_list: # List insert
            sel_list.insert(0,c)

        label_output.append(sel_list)
    
for i in range(3):
    clear_output(wait=True) # 창 초기화
    print('------------------------------[ '+str(i+1)+'번째 게시글 ]------------------------------')
    labeling(str(test_list[i][0]),str(test_list[i][1]),str(test_list[i][2]),str(test_list[i][3]))
    
label_df = pd.DataFrame(label_output)
label_df.columns = ['장소','본문','태그','1.가볼만한곳','2.가족여행', '3.우정여행', '4.전통','5.체험', '6.캠핑','7.관람','8.맛집', '9.카페']
finsih_alram()
label_df.to_excel('라벨링완료_'+file_name+'.xlsx')