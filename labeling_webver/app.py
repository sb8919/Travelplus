# -*- coding: utf-8 -*-
import socket
from flask import Flask, request, jsonify
from flask import render_template, send_file
import urllib.request
import pymysql
import dbcl
import os
import to_excel
import upload_data
import merge_xlsx


app = Flask(__name__)

userdb = dbcl.DBconnector('user')
labeling = dbcl.DBconnector('label_Data')

def save_img(data):
    path='static/img/pic.png'
    try:
        urllib.request.urlretrieve(data[2], path)
    except:
        urllib.request.urlretrieve('https://cdn-icons-png.flaticon.com/512/3875/3875148.png', path)
    
@app.route("/") 
def index():
    return render_template('index.html')

@app.route("/work_on", methods=['GET','POST']) 
def work_on():
    try:
        name = request.args.get('name')
        lb_st_num = userdb.fetch_one("SELECT start_label FROM user WHERE name='%s'"%name)
        lb_end_num = userdb.fetch_one("SELECT end_label FROM user WHERE name='%s'"%name)
        data = labeling.fetch_all("SELECT Contents, HashTag, img_url, location FROM labeling WHERE No=%s"%lb_st_num)
        data = data[0]
        content=data[0]
        hashtag=data[1]
        save_img(data)
        if lb_st_num >= lb_end_num:
            return '할당량을 다 마쳤습니다'
        else:
            percent = int(((700-(lb_end_num-lb_st_num)) /700 ) * 100)
            return render_template('work.html',content=content, hashtag= hashtag,name = name,percent=percent)
    except TypeError:
        return render_template('unknown.html')

@app.route("/work_start", methods=['GET','POST']) 
def work_start():
    name = request.args.get('name')
    label = request.args.get('label')
    lb_num = userdb.fetch_one("SELECT start_label FROM user WHERE name='%s'"%name)
    data = labeling.fetch_all("SELECT Contents, HashTag, img_url, location FROM labeling WHERE No=%s"%(int(lb_num)+1))
    lb_st_num = userdb.fetch_one("SELECT start_label FROM user WHERE name='%s'"%name)
    lb_end_num = userdb.fetch_one("SELECT end_label FROM user WHERE name='%s'"%name)
    labeling.update("UPDATE labeling SET label ='%s' where No=%s"%(label,lb_num))
    userdb.update("UPDATE user SET start_label ='%s' where name = '%s'"%((int(lb_num)+1),name))
    if lb_end_num <= lb_st_num:
        return '할당량을 완료했습니다.'
    try:
        data = data[0]
        content=data[0]
        hashtag=data[1]
        save_img(data)
    except IndexError:
        return render_template("index.html")
    percent = int(((700-(lb_end_num-lb_st_num)) /700 ) * 100)
    return render_template("work.html",content=content, hashtag= hashtag ,name = name, percent=percent )
    
@app.route("/file_download") 
def file_download():
    file_data = labeling.fetch_all("SELECT * FROM labeling WHERE label != 'None'")
    to_excel.file_download(file_data)
    path = '/root/web/static/data/labeling_data.xlsx'
    return send_file(path,as_attachment=True)   


@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join('/root/web/static/data/upload/', 'upload.xlsx'))
        upload_data.insert_data_to_db()
        return render_template('index.html')   
    return render_template('file_upload.html')    

@app.route('/init_index')
def init_index():
    labeling.execute('ALTER TABLE label_Data.labeling AUTO_INCREMENT = 1;')
    return '초기화 완료'

@app.route('/merge_upload', methods=['GET', 'POST'])
def merge_upload():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            filename = file.filename
            file.save(os.path.join('/root/web/static/data/merge/', filename))
        merge_xlsx.merge_start()
        path = '/root/web/static/data/merge/'
        for filename in os.listdir(path):
            file_path = os.path.join(path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
        return send_file(path+'complete/complete.xlsx',as_attachment=True)
    else:
        return render_template('file_upload.html')
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=3000)
