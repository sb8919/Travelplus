import pandas as pd
import os
import tkinter as tk

df_list = pd.DataFrame()
file_list = os.listdir(os.path.abspath('data')) #데이터 폴더에서 파일 목록 추출
c,d = 0,0 #포인터
number = 4 #나눌 사람 수

divide = int(len(file_list)/number)
for i in range(4):
    df_list = pd.DataFrame()
    d += divide
    for f in file_list[c:d]:
        df = pd.read_excel('data/'+f,usecols=[1,2,3,4]) #파일 각 불러오기
        df_list = pd.concat([df_list, df]) #df_list 데이터프레임에 합치기
        
    out_df = [] #각 합치는 출력 데이터 프레임
    hash_tmp = [] #중복을 방지하기위한 임시저장소(해시태그)
    con_tmp = [] #중복을 방지하기위한 임시저장소(본문)

    for df in range(len(df_list)):
        if df == 0:
            pass
        else:
            hash_tmp.append(df_list.iloc[df-1]['해시태그'])
            con_tmp.append(df_list.iloc[df-1]['본문'])
            if df_list.iloc[df]['해시태그'] in hash_tmp or df_list.iloc[df]['본문'] in con_tmp: # 임시저장소에 값이 있나 중복 검사
                continue
            else:
                if df_list.iloc[df]['해시태그'] =='[]': #해시태그가 공란인 경우
                    continue
                else:
                    out_df.append([df_list.iloc[df]['이미지URL'],df_list.iloc[df]['장소'],df_list.iloc[df]['본문'],df_list.iloc[df]['해시태그'][1:-1]]) #해시태그 전처리
                    
    out_df =pd.DataFrame(out_df) # 최종출력 데이터프레임 생성
    out_df = out_df.dropna() # 값이 없는 값 삭제
    out_df.columns = ['이미지URL','장소','본문','해시태그']
    out_df.reset_index(drop = True, inplace = True)
    out_df.to_excel('MergeCrolling['+str(i)+']_크롤링.xlsx')
    c += divide
    