import pandas as pd
import random

def file_download(data):
    content = []
    hashtag = []
    place = []
    label = []
    for i in range(len(data)):
        if (len(data[i][4]) == 1):
            content.append(data[i][1])
            hashtag.append(data[i][2])
            place.append(data[i][5])
            label.append(data[i][4])
        else:
            multi_label = data[i][4].split(',')
            for m in multi_label:
                content.append(data[i][1])
                hashtag.append(data[i][2])
                place.append(data[i][5])
                label.append(m)

    df = pd.DataFrame({'본문': content, '태그': hashtag, '장소': place, '라벨': label})

<<<<<<< HEAD
    path = '/root/web/Travelplus/labeling_webver/static/data/labeling_data.xlsx'
    
    df.to_excel(path)
    
    return print('엑셀 변환 완료')

def file_download_one(data):
    content = []
    hashtag = []
    place = []
    label = []
    for i in range(len(data)):
        if (len(data[i][4]) == 1):
            content.append(data[i][1])
            hashtag.append(data[i][2])
            place.append(data[i][5])
            label.append(data[i][4])
        else:
            multi_label = data[i][4].split(',')
            content.append(data[i][1])
            hashtag.append(data[i][2])
            place.append(data[i][5])
            random.shuffle(multi_label)
            label.append(multi_label[0])

    df = pd.DataFrame({'본문': content, '태그': hashtag, '장소': place, '라벨': label})

    path = '/root/web/Travelplus/labeling_webver/static/data/labeling_data.xlsx'
=======
    path = '/root/web/Travel_plus_parsing_web/static/data/labeling_data.xlsx'
>>>>>>> b420f42b34f0016ef9e2661bc5da219e3d7ed309
    
    df.to_excel(path)
    
    return print('엑셀 변환 완료')