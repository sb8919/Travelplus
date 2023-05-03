import pandas as pd
from collections import Counter

# 엑셀 파일 읽어들이기
df = pd.read_excel('목포근대역사관_크롤링.xlsx')
most_tag = ''

# 4열에서 해시태그만 추출하여 리스트에 저장
hashtags = []
for cell in df.iloc[:, 4]:
    tags = [tag for tag in cell.replace("'",' ').replace("[",'').replace("]",' ').replace(" ",'').split(',')]
    hashtags.extend(tags)
# 빈도 계산
counter = Counter(hashtags)

# 빈도가 높은 순으로 상위 10개 해시태그 출력
for tag, count in counter.most_common(20):
    print(tag, count)
    most_tag+= ' ' + tag
print(most_tag)