from bs4 import BeautifulSoup
from selenium import webdriver
driver = webdriver.Chrome()
driver.get('http://my.knu.ac.kr/stpo/stpo/cour/plans/viewPlanDetail.action?plans.searchOpenYrTrm=%2720172%27&plans.searchSubjCde=%27CLTR211%27&plans.searchSubClassCde=%27001%27&search_subj_area_cde=13&search_open_yr_trm=20172')

html = driver.page_source
soup = BeautifulSoup(html,"html.parser")
table = soup.find("table", {"class": "form1"})

trs=table.find_all('td')
i=0;
temp=['objective','textbook','description','criteria','notice','disabilities']
summary={}
for tr in trs:
    result=""
    for e in tr.findAll('br'):
        e.extract()
        
    ps=tr.findAll('p')

    for e in tr.findAll('p'):
        e.extract()
    if(tr.string):
        result=result+tr.string
    for p in ps:
        if(len(p)!=0):
            result=result+p.string
    summary[temp[i]]=result
    print(result)
    print('-----')
    i=i+1


