import json

from pandas import DataFrame
from urllib.request import urlopen
from bs4 import BeautifulSoup

value=[]
sub01_values=[]
sub02_values=[]
sub03_values=[]
sub04_values=[]


value.append(sub01_values)
value.append(sub02_values)
value.append(sub03_values)
value.append(sub04_values)

main_url= urlopen("http://my.knu.ac.kr/stpo/stpo/cour/listLectPln/list.action");
soup= BeautifulSoup(main_url,"html.parser")

i=0;
selects = soup.findAll('select',{"class" : "sub"})
for select in selects:
    options=select.find_all('option')
    for option in options:
        temp=option['value'];
        if temp=="":
            continue
        value[i].append(temp)
        
        
    i=i+1
#sub 2~4에 대해 3번째 옵션을 json형식에서 취함

json_url1='http://my.knu.ac.kr/stpo/stpo/cour/listLectPln/listCrseCdes2.action?search_open_bndle_cde='
json_url2='&search_gubun=1'

i=1

select='open_crse_cde_'
while i<=3:
    total=[]
    for code in value[i]:
        temp=[]
        temp2=[]
        temp.append(code)
        complete_url=json_url1+code+json_url2
        html =urlopen(complete_url)
        soup2 = BeautifulSoup(html,"html.parser")
        datas=json.loads(str(soup2).replace("'",'"'))
        if len(datas)==0:
            continue
        for data in datas:
            j=1;
            length=len(data)/2
            while j<=length:
                temp2.append(data[select+str(j)])
                j=j+1
        temp.append(temp2)
        total.append(temp)

    value[i]=total
    i=i+1

print(value[0])
print("-----------------------------")
print(value[1])
print("-----------------------------")
print(value[2])
print("-----------------------------")
print(value[3])
print("-----------------------------")

    






                
                
            




