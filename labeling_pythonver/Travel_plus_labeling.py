import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from skimage import io
import matplotlib.pyplot as plt
from IPython.display import clear_output
from tkinter import filedialog
import easygui


data_file_path = easygui.fileopenbox()
x = data_file_path.split('\\')
x.reverse()
fn = x[0].split('.')
file_name = fn[0]


df = pd.read_excel(data_file_path, engine = "openpyxl")
arr = np.array(df)
df_list = np.delete(arr, 0, axis = 1)
#test_list = [['장소','본문','태그','img_url'],['장소2','본문2','태그2','img_url2'],['장소3','본문3','태그3','img_url3'],] #입력리스트 ex) 엑셀 데이터
label_output = [] #출력리스트
theme = 9 #테마 개수(스팸 포함)

list_count = len(df_list) # Count List

def finsih_alram(): # notice over
    print('----------------------------------------------------\n\n\t\t\t라벨링완료\n\n----------------------------------------------------')

def get_df(sel,tags,main,place): # append label_output(tuple)
            
    sel_list = [sel]   
        
    content_output_list = [tags,main,place] # list to add to Excel
    
    for c in content_output_list: # List insert
        sel_list.insert(0,c) 

    label_output.append(sel_list) # make tuple ex) ['장소','본문','태그',0,1,0,0,0,0,0,0]

def mkdf(): # make DataFrame
    label_df = pd.DataFrame(label_output)
    label_df = pd.DataFrame(label_df)
    label_df.columns = ['장소','본문','태그','테마']
    return label_df       

def labeling(url,place,main,tags):
    # URL Error exception handling
    try:
        image = io.imread(url)
        plt.imshow(image)
        plt.show()
    except:
        print('이미지출력 : 안됨')
        
    print('장소 : '+ place)
    print('본문 : '+ main)
    print('태그 : '+ tags)   
    sel = input("\n라벨링 해주세요 1.가볼만한곳 2.가족여행 3.우정여행 4.전통 5.체험 6.캠핑 7.관람 8.맛집 9.카페 0.스팸 [일시중지하기 : s] \n")
    
    if sel == '0':# Pass when spam
        return
    else:
        if sel == "s": # Stop
            return sel
        else:
            get_df(sel,tags,main,place)

save_index=0       
list_count = list_count

for i in range(save_index, list_count):
    clear_output(wait=True) # Clear cell
    print('------------------------------[ '+str(i+1)+'번째 게시글 ]------------------------------')
    sel = labeling(str(df_list[i][0]),str(df_list[i][1]),str(df_list[i][2]),str(df_list[i][3]))
    if sel == 's':
        print('--------------------!일시중지!-----------------------\n')
        print(str(i)+'번째에서 일시중지 하였습니다.\n')
        break
        
if sel =='s':
    label_df = mkdf()
    label_df.to_excel('라벨링tmp_'+file_name+'.xlsx')
else:
    label_df = mkdf()
    label_df.to_excel('라벨링완료_'+file_name+'.xlsx')
finsih_alram()