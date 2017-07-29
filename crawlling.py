# -*- coding: utf-8 -*-

import pymysql
import urllib.request
from bs4 import BeautifulSoup
from selenium import webdriver
domain = "http://my.knu.ac.kr"

conn = pymysql.connect(host="211.253.11.80",
                           user="root",
                           password="rudeofldk17!",
                           db="knutime",
                           charset="utf8")
cursor = conn.cursor(pymysql.cursors.DictCursor)

conn2 = pymysql.connect(host="211.253.11.80",
                           user="root",
                           password="rudeofldk17!",
                           db="timetable",
                           charset="utf8")
cursor2 = conn2.cursor(pymysql.cursors.DictCursor)

count=1

# BeautifulSoup 생성
def create_bs(url):
    req = urllib.request.Request(url)
    data = urllib.request.urlopen(req).read()

    return BeautifulSoup(data, "html.parser")

# 모든 과정 Url 가져옴
def get_univ_url(year):
    link = domain + "/stpo/stpo/cour/listLectPln/list.action"
    urls = []

    sql = "SELECT * FROM dept_url WHERE depth1_code=02 and depth2_code=16"
    cursor.execute(sql)

    rows = cursor.fetchall()

    for row in rows:
        url = link

        depth2_code = row['depth2_code']
        depth3_code = row['depth3_code']
        param1 = row['parameter1']
        param2 = row['parameter2']
        param3 = row['parameter3']

        if param2 is not None:
            url += '?' + param2 + '=' + depth2_code

        if param1 is not None:
            url += '&' + param1 + '=' + year

        if param3 is not None:
            url += '&' + param3 + '=' + depth3_code

        urls.append(url)

    return urls

# 학과별 과목 link를 가져옴
def get_course_url(url):
    bs = create_bs(url)

    links = []

    tds = bs.find_all("td", class_="th4")

    for td in tds:
        link = td.find("a")
        links.append(link["href"].replace("Eng", ""))

    return links

def refine_data(td):
    l = list(td.stripped_strings)

    if len(l) == 1:
        return l[0]
    else:
        return l

def get_summary(url):
    bs = create_bs(url)
    summary = {}
    summary['check']='a'
    table = bs.find("table", id="form2")
    rows = table.find_all('tr')

    
          
    summary["course_title"] = refine_data(rows[0].find('td'))
    summary["course_code"] = refine_data(rows[1].find('td'))
    summary["credits"] = refine_data(rows[2].find('td'))
    summary["department"] = refine_data(rows[3].find('td'))
    summary["semester"] = refine_data(rows[4].find('td'))
    summary["course_categories"] = refine_data(rows[5].find('td'))
    summary["instructor"] = refine_data(rows[6].find('td'))
    hour=""
    for e in refine_data(rows[7].find('td')) :
        hour=hour+e+", "
    
    summary["hours"] = hour[:-2]
    summary["location"] = refine_data(rows[8].find('td'))
    summary["phone_email"] = refine_data(rows[9].find('td'))
    summary["office_hours"] = refine_data(rows[10].find('td'))
    summary["language"] = refine_data(rows[11].find('td'))
      
    

    
    if summary['course_code'].find('CLTR')>-1 or summary['course_code'].find('TCHR')>-1 :
        summary['check']='b'
        return summary;
    
    driver = webdriver.Chrome()
    driver.get(url)

    html = driver.page_source
    soup = BeautifulSoup(html,"html.parser")
    table = soup.find("table", {"class": "form1"})

    trs=table.find_all('td')
    i=0;
    temp=['objective','textbook','description','criteria','notice','disabilities']
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
            if p.string == None :
                continue;
            if len(p)!=0:
                result=result+p.string
        summary[temp[i]]=result
        i=i+1

    
    return summary

def tf(data):
    if type(data) is list:
        if len(data) == 0:
            return ""
        return data[0]
    else:
        return data

def store_data_to_database(year):
    sql = "INSERT INTO Class VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    sql2 = "INSERT INTO Syllabus VALUES(%s, %s, %s, %s, %s, %s, %s)"
    univ_urls = get_univ_url(year)
    for univ_url in univ_urls:
        course_urls = get_course_url(univ_url)
        
        for course_url in course_urls:
            result = get_summary(domain + course_url)
            if result['check']=='b':
                continue;
            
            course_title = tf(result["course_title"])
            course_code = tf(result["course_code"])
            credits = tf(result["credits"])
            department = tf(result["department"])
            semester = tf(result["semester"])
            course_categories = tf(result["course_categories"])
            instructor = tf(result["instructor"])
            hours = tf(result["hours"])
            location = tf(result["location"])
            phone_email = tf(result["phone_email"])
            office_hours = tf(result["office_hours"])
            language = tf(result["language"])

            cursor2.execute(sql,
                           (course_code,course_title,
                           credits, department,
                           semester, course_categories,
                           instructor, hours,
                           location, phone_email,
                           office_hours, language))
            conn2.commit()
            
            objective=result['objective']
            textbook=result['textbook']
            description=result['description']
            criteria=result['criteria']
            notice=result['notice']
            disabilities=result['disabilities']

            cursor2.execute(sql2,
                           (course_code,objective,textbook,description,
                            criteria,notice,disabilities))
            conn2.commit()

            
    conn2.close()

           

store_data_to_database('20172')
