import json
import urllib.request
from bs4 import BeautifulSoup

url='http://my.knu.ac.kr/stpo/stpo/cour/listLectPln/listCrseCdes2.action?search_open_bndle_cde=13&search_gubun=1'
html =urllib.request.urlopen(url)
soup = BeautifulSoup(html,"html.parser")
#r=html.read()
#'https://api.github.com/users?since=0'

data=json.loads(str(soup).replace("'",'"'))

print(data[1])

