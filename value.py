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

def get_summary(url):
    url2=urlopen(url)
    soup= BeautifulSoup(url2,"html.parser")

    links=[]

    base_url="http://my.knu.ac.kr/"
    tds=soup.find_all("td",{"class" : "th4"})
    for td in tds :
        link1=td.find("a")
        links.append(link1["href"])



    summary =[]

    for link in links :
        newlink=base_url+link;
        url2=urlopen(str(newlink))
        soup2= BeautifulSoup(url2,"html.parser")

        course=[]

        table=soup2.find("table",{"id" : "form2"})
        trs=table.find_all("tr");
        i=1
        for tr in trs :
            course.append(tr.find("th").string)
            course.append(tr.find("td").string)
            i=i+1
            if i==13 :
                break

        summary.append(course)

    return summary


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
    
total_summary=[];

url1="http://my.knu.ac.kr/stpo/stpo/cour/listLectPln/list.action?search_open_crse_cde="
url2="&sub="
url3="&search_open_yr_trm=20172"
for code in value[1] :
    for dept in code[1] :
        newurl=url1+str(dept)+url2+str(code[0])+url3
        temp=get_summary(newurl)
        print(temp)
        total_summary.append(temp)

print(total_summary)
        
                






                
                
            




