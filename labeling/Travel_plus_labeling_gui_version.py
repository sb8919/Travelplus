from tkinter import *
from tkinter import ttk
import pandas as pd
import numpy as np
from tkinter import filedialog
from PIL import Image, ImageTk
import tkinter as tk
import tkinter.font
import urllib.request
from urllib.request import Request, urlopen
from urllib.error import URLError, HTTPError
from io import BytesIO
import time
import keyboard
import os
import shutil
import threading
from pathlib import Path

key = 0
label_output = [] #출력리스트
sel_theme = []
theme_conv = ['가볼만한곳','가족여행','우정여행','전통','체험','캠핑','관람','맛집','카페']

def finish_alram(): # notice over
    tk.messagebox.showinfo('라벨링완료', '라벨링이 완료 되었습니다.')    
    
def tmp_alaram():
    tk.messagebox.showinfo('라벨링임시저장', '라벨링이 임시저장이 완료 되었습니다.')
    
def not_selecting_alarm():
    tk.messagebox.showerror('선택오류', 'Error: 파일을 선택하지 않았습니다!')
    
def get_df(sel,tags,main,place): # append label_output(tuple)  
    global sel_columns
    sel_list = [sel]
    content_output_list = [tags,main,place] # list to add to Excel
    
    for c in content_output_list: # List insert
        sel_list.insert(0,c) 
    
    label_output.append(sel_list) # make tuple ex) ['장소','본문','태그',4]
    sel_columns = len(label_output)-2
    return sel_columns

def mkdf(): # make DataFrame   
    label_df = pd.DataFrame(label_output)
    label_col1 = ['장소','본문','태그']
    return label_df

def start_position(s):
    global i
    i = s
    
def KeyClick(labeling_win,file_name,data_file_path,process_label,photo_label,place_label,content_label,tags_label,df_len,df,df_list):
    allow_list=['1','2','3','4','5','6','7','8','9']
    global sel_theme
    global i
    zero_working = True
    was_pressed = False
    
    URL=df_list[i][0]
    place = df_list[i][1]
    main = df_list[i][2]
    tags = df_list[i][3]
    if i == 0:
        URL=df_list[0][0]
        place = df_list[0][1]
        main = df_list[0][2]
        tags = df_list[0][3]
        if keyboard.is_pressed('s'):
            tk.messagebox.showinfo('라벨링임시저장', '첫번째 게시물은 저장할 수 없습니다.')

        elif keyboard.is_pressed('p'):
            if not was_pressed:
                get_df(sel_theme,tags,main,place)
                sel_theme = [] 
                i += 1
                was_pressed = True
            else:
                was_pressed = False
        elif keyboard.is_pressed('0'):
            if zero_working == False:
                pass
            else:
                get_df(['스팸'],tags,main,place)
                i += 1
        else:
            for k in allow_list:
                if keyboard.is_pressed(k):
                    if not was_pressed:
                        th = theme_conv[int(k)-1]
                        sel_theme.append(th)
                        was_pressed = True
                        zero_working = False
                    else:
                        was_pressed = False
                    

    else:
        if keyboard.is_pressed('s'):
            label_df = mkdf()
            label_df.loc[len(label_df)]=[df_len,'','','']
            if st>0:
                label_df.to_excel('라벨링tmp_'+file_name.split('_')[1]+'_크롤링.xlsx')
            else:
                label_df.to_excel('라벨링tmp_'+file_name+'.xlsx')
            tmp_alaram()
            labeling_win.destroy()
            return    

        elif keyboard.is_pressed('p'):
            if not was_pressed:
                get_df(sel_theme,tags,main,place)
                sel_theme = [] 
                i += 1
                was_pressed = True
            else:
                was_pressed = False
        elif keyboard.is_pressed('0'):
            if zero_working == False:
                pass
            else:
                get_df(['스팸'],tags,main,place)
                i += 1
        else:
            for k in allow_list:
                if  keyboard.is_pressed(k):
                    if not was_pressed:
                        print(k)
                        th = theme_conv[int(k)-1]
                        sel_theme.append(th)
                        was_pressed = True
                    else:
                        was_pressed = False

    #출력 부분(다음내용 업데이트)
    if i <= df_len: 
        try:
            global u
            global raw_data
            URL=df_list[i][0]
            place = df_list[i][1]
            main = df_list[i][2]
            tags = df_list[i][3]
            headers = {'User-Agent':'Chrome/66.0.3359.181'}
            req = urllib.request.Request(URL, headers=headers)
            u = urllib.request.urlopen(req)
            raw_data = u.read()
            u.close()
            process_label.config(text='--------------------- 진행상황 '+str(i)+'/'+str(df_len)+' ---------------------')
            img2 = ImageTk.PhotoImage(Image.open(BytesIO(raw_data)).resize((500, 500), Image.ANTIALIAS))
            photo_label.config(image=img2)
            photo_label.image = img2
            place_label.config(text="장소 :"+str(place))    
            content_label.config(text="본문 :"+str(main))    
            tags_label.config(text="태그 :"+str(tags)) 
        except HTTPError as e:
            err = e.read()
            code = e.getcode()
    else:
        label_df = mkdf()
        if st > 0:
            os.remove(data_file_path)
            label_df.to_excel('라벨링완료_'+file_name.split('_')[1]+'.xlsx')
        else:
            label_df.to_excel('라벨링완료_'+file_name+'.xlsx')
        finish_alram()

        labeling_win.destroy()

                       
        
def open_file():
    label_output.clear()
    try:
        data_file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("Excel File", "*.xlsx"),("all files", "*.*")))
        file_is =Path(data_file_path)
        file_name = data_file_path.split('/')[-1].split('.')[0]
        df = pd.read_excel(data_file_path, engine = "openpyxl")
        df_len=int(df.iloc[-1][0])
        arr = np.array(df)
        df_list = np.delete(arr, 0, axis = 1)
        global st  
        st = len(df)
        if "tmp" not in file_name:
            if (file_is.is_file()):
                pass
            else:
                shutil.copy(data_file_path,os.getcwd()+"/"+file_name+".xlsx")
            st = 0
        else:
            st = int(st-1) 
            count = 0
            try:
                df = pd.read_excel(file_name.split('_')[1]+'_크롤링.xlsx', engine = "openpyxl")
            except FileNotFoundError:
                tk.messagebox.showerror('파일오류', 'Error: 원본파일과 tmp파일의 위치를 같게 해주세요!')
            df_len=int(df.iloc[-1][0])
            for dl in df_list[:-1]:
                label_output.append(dl)
            print(label_output)
            arr = np.array(df)
            df_list = np.delete(arr, 0, axis = 1)
        start_position(st)
        return file_name,df,df_len,df_list,data_file_path
    except FileNotFoundError:
        not_selecting_alarm()
        
def update_process(i,process_label,df_len):
    process_label.config(text='--------------------- 진행상황 '+str(i)+'/'+str(df_len)+' ---------------------')
    
def start_labeling():
    try:
        file_name,df,df_len,df_list,data_file_path = open_file()
    except TypeError:
        return
    labeling_win = Toplevel()
    labeling_win.resizable("FALSE","TRUE")
    labeling_win.title("LabelStagram")
    URL=df_list[st][0]
    place = df_list[st][1]
    main = df_list[st][2]
    tags = df_list[st][3]
    
    try:
        global u
        global raw_data
        headers = {'User-Agent':'Chrome/66.0.3359.181'}
        req = urllib.request.Request(URL, headers=headers)
        u = urllib.request.urlopen(req)
        raw_data = u.read()
        u.close()
        im = Image.open(BytesIO(raw_data))
        im = im.resize((500, 500), Image.ANTIALIAS)
        photo = ImageTk.PhotoImage(im)
    except HTTPError as e:
        err = e.read()
        code = e.getcode()
        
    
    try:
        photo_label = tk.Label(labeling_win,image=photo,width=500,height=500)
        photo_label.image = photo
    except UnboundLocalError:
        photo_label = tk.Label(labeling_win,text='사진없음',height=25)
        
    process_label = tk.Label(labeling_win, text='--------------------- 진행상황 0/'+str(df_len)+' ---------------------')
    process_label.grid(column = 0, row= 0, pady = (15,0), sticky='wes')
    update_process(i,process_label,df_len)
    photo_label.grid(column=0,row=1,padx=20,pady=20)
    place_label= tk.Label(labeling_win,text="장소: "+str(place))
    place_label.grid(column=0,row=2,sticky='w')
    content_label=tk.Label(labeling_win,text="본문: "+str(main),wraplength = 550)
    content_label.grid(column=0,row=3,sticky='w')
    tags_label= tk.Label(labeling_win,text="태그: "+str(tags),wraplength = 550, fg='RoyalBlue3')
    tags_label.grid(column=0,row=4,sticky='w')
    guide_text1= tk.Label(labeling_win,text="키보드로 입력해주세요😁")
    guide_text1.grid(column=0,row=5)
    guide_text= tk.Label(labeling_win,text="1.가볼만한곳 2.가족여행 3.우정여행 4.전통 5.체험 6.캠핑 7.관람 8.맛집 9.카페 0.스팸 [일시중지하기 : s]")
    guide_text.grid(column=0,row=6)
    labeling_win.bind("<Key>",lambda event: KeyClick(labeling_win,file_name,data_file_path,process_label,photo_label,place_label,content_label,tags_label,df_len,df,df_list))
    
#File_status
def load_file():
    try:
        filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select file", filetypes=(("Excel File", "*.xlsx"),("all files", "*.*")))
        if(filename.find('완료')!=-1):
            bar_index=100
            per=str(bar_index)
        else:
            tmp = pd.read_excel(filename)
            tmp_arr = np.array(tmp)
            tmp_value = np.delete(tmp_arr, 0, axis = 1)
            label_check = len(tmp_value)-1
            label_max = tmp.iloc[-1][1]
            if type(label_check) is str or type(label_max) is str:
                bar_index = 0
            else:
                filename= filename.split('/')[-1].split('.')[0]
                view_content.configure(text=filename+'의 진행상황은')
                bar_index = label_check/label_max * 100
            per = str(int(bar_index))
        bar['value'] = bar_index
        view_percent.configure(text=per+'%')
    except FileNotFoundError:
        not_selecting_alarm()
        
def now_dir():
    dir = os.getcwd()
    os.startfile(dir)
    
win = Tk()
win.geometry("400x200+500+400")
win.title("Labeling Program")
#Font style
title=tk.font.Font(family="맑은 고딕", size=18, weight='bold')
content=tk.font.Font(family="맑은 고딕", size=10)
percent=tk.font.Font(family="맑은 고딕", size=20)
load_font=tk.font.Font(family="맑은 고딕", size=10, weight='bold')
#win style
win.configure(bg='gray5')
win.columnconfigure(0,weight=1)
win.rowconfigure(0,weight=1)
#main_Frame(view_status_Frame, work_labeling_Frame)
main_Frame = Frame(win, bg = 'gray15')
main_Frame.grid(row = 0, column = 0 ,  sticky='WESN')
#main_Frame style
main_Frame.columnconfigure(0,weight=3)
main_Frame.columnconfigure(1,weight=1)
main_Frame.rowconfigure(0,weight=1)
#view_status_Frame
view_status_Frame = Frame(main_Frame, bg='gray22')
view_status_Frame.grid(row=0, column=0, padx =10 , pady = 10 , ipadx=20, ipady=10, sticky='WESN')
#view_status_Frame_function
view_title = Label(view_status_Frame, text="STATUS", bg='gray22', fg='white', font= title)
view_title.grid(row=0, column=0, sticky='w',padx=10)
view_content = Label(view_status_Frame, text="선택하신 파일의 진행상황은", bg='gray22', fg='white' ,font=content)
view_content.grid(row=1, column=0, sticky='w',padx=10)
view_content2 = Label(view_status_Frame, text="아래와 같습니다.", bg='gray22', fg='white' ,font=content)
view_content2.grid(row=2, column=0, sticky='w',padx=10)
view_percent = Label(view_status_Frame, text="0%", bg='gray22', fg='white' ,font=percent)
view_percent.grid(row=3, column=0, sticky='w',padx=10)
#percent
s = ttk.Style()
s.theme_use('alt')
s.configure("black.Horizontal.TProgressbar",troughcolor ='gray40', background='dodger blue', thickness=30)
bar = ttk.Progressbar(view_status_Frame, length=200, s='black.Horizontal.TProgressbar')
bar['value'] = 1
bar.grid(row=4, column=0, pady=10, padx= (12,0), sticky='w')
#work_labeling_Frame
work_labeling_Frame = Frame(main_Frame, bg='gray22')
work_labeling_Frame.grid(row=0, column = 1, padx =(0,10) , pady = 10 , ipadx=10, ipady=10, sticky='WESN')
#work_labeling_Frame style
work_labeling_Frame.columnconfigure(0,weight=1)
#work_labeing_Frame_function
button_font=tk.font.Font(family="맑은 고딕", size=10, weight='bold')
new_btn = Button(work_labeling_Frame,text=" Sel File",bg='gray28',fg='white', font = button_font, command=start_labeling)
new_btn.grid(row=0,column=0 ,pady=8,sticky='we')
file_status = Button(work_labeling_Frame,text=" File Status", bg='gray28',fg='white', font = button_font ,command=load_file)
file_status.grid(row=2,column=0 ,pady=8,ipadx=5,sticky='we')
open_btn = Button(work_labeling_Frame,text=" Open Dir", bg='gray28',fg='white', font = button_font, command = now_dir )
open_btn.grid(row=3,column=0 ,pady=8,ipadx=5,sticky='we')
#Icon Setting
try:
    new_file = PhotoImage(file='add.png')
    new_btn.config(image=new_file, compound=LEFT)
    small_logo1 = new_file.subsample(20, 20)
    new_btn.config(image=small_logo1)
    
    load_file_ic = PhotoImage(file='loading.png')
    load_btn.config(image=load_file_ic, compound=LEFT)
    small_logo2 = load_file_ic.subsample(20, 20)
    load_btn.config(image=small_logo2)
    
    open_dir = PhotoImage(file='folder.png')
    open_btn.config(image=open_dir, compound=LEFT)
    small_logo3 = open_dir.subsample(20, 20)
    open_btn.config(image=small_logo3)
    
except TclError:
    print("아이콘 존재하지않음")


win.mainloop()