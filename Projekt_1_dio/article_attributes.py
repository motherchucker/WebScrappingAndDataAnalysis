import requests
import os
from bs4 import BeautifulSoup
import datetime
import time
from csv import writer
import csv
import json

'''
PODSJETNIK:

meta podaci za izvuc:

property                -  sta je unutra 
og:title                - naziv clanka
og:description          - tekst clanka
og.url                  - url clanka
article:published_time  - datum objave
article:modified_time   - modificirani datum objave


izvan meta:
unutar div class = meta-info
div td-post-views 
treba vrijednost span class= 'td-nr-views-{6}, sadrzi broj gledanja posta

span class="_5n6h _2pih id=u_0_2      , sadrzi broj lajkova posta

td-post-author-name unutar a href-a vrijednost ima ime autora (npr sp)

td-post-source-tags td-pb-padding-side sadrze tagove unutar ul -> [li] 
u li se nalaze kao vrijednost od <a>

td-post-header td-pb-padding-side , unutar ul class=td-category vrijednost <a> je kategorija

idlink = countLinks
title = ''
author = ''
url = ''
category = ''
textArticle = ''
published_date = ''
modified_date = ''
nviews = ''
nlike = ''
tags = ''
'''


# Ucitavanje linkova 
linkovi_txt = open('rijekadanas_linkovi.txt', 'r')
linkovi = linkovi_txt.readlines()
nlinks = len(linkovi)
print('Number of links loaded:  ',nlinks)

countLinks = 1 

def listToString(lista):
    razmak = '\n'
    return(razmak.join(lista))


#Timer
start = time.time()

if os.path.exists('rijekadanas.csv'):
    os.remove('rijekadanas.csv')

# .csv file
with open('rijekadanas.csv', 'a', encoding= 'utf-8') as csv_file:
    csv_writer = writer(csv_file, delimiter= ',', quotechar= '"', quoting = csv.QUOTE_NONNUMERIC, lineterminator= '\n')
    headers = ['ID', 'Title', 'Author', 'URL', 'Category', 'Text', 'Published_date', 'Modified_date', 'Views', 'Likes', 'Tags']

    csv_writer.writerow(headers)

    requests_session = requests.Session()

    for link_ in linkovi:
        #IZVLACENJE PODATAKA SA JEDNOG CLANKA ---- TEST

        #response = requests_session.get(linkovi[1117])
        #print(response)
        #response = requests_session.get('https://www.rijekadanas.com/video-koji-pokazuje-kako-se-lako-virus-siri-u-restoranu-postao-viralan/')  #sa tagom
        #print(response.status_code)
        response = requests_session.get(link_, headers={'User-Agent' : 'Mozilla/5.0'})

        print('Finished links: ',str(countLinks),'/',nlinks)
        print('Now processing : ', link_)

        #check site status
        if response.status_code != 200:
            print('Error code: ', str(response.status_code))
        else:
            soup = BeautifulSoup(response.text, 'lxml')

            idlink = countLinks
            title = ''
            author = ''
            url = ''
            category = ''
            textArticle = ''
            published_date = ''
            modified_date = ''
            nviews = ''
            nlike = ''
            tags = ''

            #naziv clanka
            title = soup.find('meta',property='og:title').get('content')
            #print('Title:  ',title)
            
            #autor
            for a in soup.find_all(class_='td-post-author-name'):
                author = a.find('a').text
                #print('Author:  ',author)

            #url
            url = soup.find('meta', property='og:url').get('content')
            #print('Url:  ',url)

            #kategorija
            for c in soup.find_all(class_='td-category'):
                category = c.find('a').text
                #print('Category:  ',category)

            #tekst
            content = soup.find_all(class_='td-post-content')
            cijeliTekst = []
            for t in content:
                for p in t.find_all('p'):
                    if(p.text == ''):
                        continue
                    cijeliTekst.append(p.text)
            #lista --> string
            textArticle = listToString(cijeliTekst)
            #print('Tekst:  \n',textArticle)

            #datum objave
            published_date = soup.find('meta', property='article:published_time',content= True).get('content')
            date_p = datetime.datetime.strptime(published_date, '%Y-%m-%dT%H:%M:%S%z')
            published_date = date_p.date()
            #print(('Published:  '),published_date)

            #datum modificirane objave
            if (soup.find('meta', property='article:modified_time',content= True)):
                modified_date = soup.find('meta', property='article:modified_time',content= True).get('content')
                date_m = datetime.datetime.strptime(modified_date, '%Y-%m-%dT%H:%M:%S%z')
                modified_date = date_m.date()
                #print(('Modified:  '),modified_date)

            #broj pogleda
            for p in soup.find_all(class_='td-post-views'):
                nviews = p.find('span').text
                #print('Post views:  ',nviews)

            #broj lajkova
            for l in soup.find_all(class_='td-post-sharing-classic'):   
                stranica = l.find('iframe').get('src')
                #print('\nsrc:  ',stranica)
                responseLike = requests.get(stranica)
                soupLike = BeautifulSoup(responseLike.text,'lxml')
                nlike = soupLike.find('span', id='u_0_2').text
                #print('Likes:  ',nlike)

            #tagovi
            sviTagovi = []
            for t in soup.footer.find_all(class_='td-post-source-tags td-pb-padding-side'):
                if(t.find('li') != None):
                    tags = t.find_all('a')
                    for t1 in tags:
                        sviTagovi.append(t1.text)
                    tags = listToString(sviTagovi)
                    #print('Tags:  \n',tags)
                else:
                    tags = ''
                    #print(tags)

            csv_writer.writerow([idlink, title, author, url, category, textArticle, published_date, modified_date, nviews, nlike, tags])

            countLinks+=1


print('\n.JSON file...........\n')

csv_file_path = 'rijekadanas.csv'
json_file_path = 'rijekadanas.json'

data = {}

with open(csv_file_path, encoding= 'utf-8') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for rows in csv_reader:
        id = rows['ID']
        data[id] = rows

with open(json_file_path, 'w', encoding= 'utf-8') as json_file:
    json_file.write(json.dumps(data, indent= 4, ensure_ascii= False))

print('JSON file created.')

linkovi_txt.close()

end = time.time()
print('\nTime spent: ', str(end-start))