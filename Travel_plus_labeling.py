import pandas as pd

test_list = [['본문','태그','img_url'],['본문2','태그2','img_url2'],['본문3','태그3','img_url3'],] #입력리스트 ex) 엑셀 데이터
label_output = [] #출력리스트
theme = 9 #테마 개수

list_count = len(test_list)

def labeling(main,tags,url):
    print('이미지출력 '+url)
    sel = input("라벨링 해주세요 1.oo 2.oo 3.oo 4.oo 5.oo 6.oo 7.oo 8.oo 9.oo \n")
    sel_list = ['1' if l+1 == int(sel) else '0' for l in range(theme)]   
    label_output.append([main,tags,sel_list])
    
for i in range(list_count):
    labeling(test_list[i][0],test_list[i][1],test_list[i][2])

print(label_output)