import pandas as pd

def file_download(data):
    content = []
    hashtag = []
    place = []
    label = []
    for i in range(len(data)):
        if (data[i][4] == 1):
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

    path = '/root/web/static/data/labeling_data.xlsx'
    
    df.to_excel(path)
    
    return print('엑셀 변환 완료')