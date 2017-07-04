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

print(value)


