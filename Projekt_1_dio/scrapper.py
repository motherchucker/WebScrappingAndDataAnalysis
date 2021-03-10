import requests
import os
from bs4 import BeautifulSoup
from csv import writer
import re
import datetime
import time


zadnjiDate = datetime.date(2019,12,31)
start = datetime.date(2020,1,1)  #2020,1,1
end = datetime.date(2020,11,30)  #2020,11,30

if os.path.exists('log.txt'):
    os.remove('log.txt')

if os.path.exists('rijekadanas_linkovi.txt'):
    os.remove('rijekadanas_linkovi.txt')

#Timer
start_time = time.time()

#Dohvacanje glavne stranice
response = requests.get('https://www.rijekadanas.com/')

soup = BeautifulSoup(response.text,'lxml')

categList = []


# Trazenje kategorija

# /(http.*?category\/\w+\/")/

for link in soup.find_all(href=re.compile(r'/category\/\w+\/$')):
    categList.append(link.get('href'))    

lista = list(dict.fromkeys(categList))
#print(lista)

print('-----------------------------------------------')
print('BROJ PRONADENIH KATEGORIJA: ', len(lista))
print('-----------------------------------------------')

log_file = open('log.txt', 'a', encoding= 'utf-8')
log_file.write('-----------------------------------------------\n')
log_file.write('BROJ PRONADENIH KATEGORIJA: ' + str(len(lista)) + '\n')
log_file.write('-----------------------------------------------\n')
log_file.close()


svi_linkovi = []
broj_sveukupno = 0
broj_clanakaKategorije = 0

broj_clanka = 0
broj_stranice = 1
zadnjiClanak = False
zadnjiClanakKategorija = False
zadnjaKategorija = False

if(zadnjiClanak == False):
    for i in range(len(lista)):
        # print("Kategorija: ",lista[i], "\n\n")
        print('-----------------------------------------------')
        print('TRENUTNA KATEGORIJA: ', lista[i])
        print('-----------------------------------------------')
        
        log_file = open('log.txt', 'a', encoding= 'utf-8')
        log_file.write('-----------------------------------------------\n')
        log_file.write('TRENUTNA KATEGORIJA: ' + str(lista[i]) + '\n')
        log_file.write('-----------------------------------------------\n')
        log_file.close()
        


        if(lista[i] == lista[-1]):
            zadnjaKategorija = True
        kategorija = lista[i]

        while(zadnjiClanakKategorija==False):

            pom = kategorija
            kategorija=kategorija +'page/'+str(broj_stranice)+'/'
            #print(kategorija)

            response = requests.get(kategorija)
            soup = BeautifulSoup(response.text, 'lxml')

            if(zadnjiClanakKategorija==False):
                # DOHVACANJE 5 NAJNOVIJIH CLANAKA
                if(broj_stranice == 1):
                    for linkoviNovi in soup.find_all('div','td-big-grid-wrapper'):
                        for link_ in linkoviNovi.find_all('div', 'td-module-thumb'):
                            link = link_.find('a')
                            provjeriLink2 = link['href']
                            response_main = requests.get(provjeriLink2)
                            soup_main = BeautifulSoup(response_main.text, 'lxml')
                            
                            #uzimanje datuma clanaka gornjeg meni-a
                            metadate_main = soup_main.find('meta', property='article:published_time',content= True).get('content')
                            #print('datum main clanka: ', metadate_main)

                            #formatiranje datuma:
                            date_m = datetime.datetime.strptime(metadate_main, '%Y-%m-%dT%H:%M:%S%z')
                            datumClankaMain = date_m.date()

                            if (start <= datumClankaMain <=end):
                                print('Trazeni najnoviji clanak.Spremanje...\n')
                                svi_linkovi.append(link['href'])

                                #zapisivanje linkova u file
                                linkovi_file = open('rijekadanas_linkovi.txt','a')
                                linkovi_file.write(str(link['href'])+'\n')
                                linkovi_file.close()

                                broj_sveukupno+=1
                                broj_clanakaKategorije+=1

                            else:
                                print('Preskacemo clanak (ne trazimo taj datum)....\n') 
                                continue


                for linkovi in soup.find_all('div','td_module_1'):
                    broj_clanka+=1
                    link = linkovi.find('a')
                    #uci u pronadeni link
                    provjeriLink = link['href']

                    noviresposne = requests.get(provjeriLink)
                    soup1 = BeautifulSoup(noviresposne.text, 'lxml')

                    #pronalazak metapodatka koji sadrzi datum objave
                    metadate = soup1.find('meta', property='article:published_time',content= True).get('content')        

                    #formatiranje datuma:
                    date_c = datetime.datetime.strptime(metadate, '%Y-%m-%dT%H:%M:%S%z')
                    datumClanka = date_c.date()

                    if (start <= datumClanka <=end):
                        print('Trazeni clanak.Spremanje...\n')
                        svi_linkovi.append(link['href'])

                        #zapisivanje linkova u file
                        linkovi_file = open('rijekadanas_linkovi.txt','a')
                        linkovi_file.write(str(link['href'])+'\n')
                        linkovi_file.close()

                        broj_sveukupno+=1
                        broj_clanakaKategorije+=1

                        if(broj_clanka==15):
                            broj_stranice+=1
                            broj_clanka=0

                    elif(datumClanka > end):
                        print('Preskacemo clanak (ne trazimo taj datum)....\n') 
                        continue
                    else:
                       #Ako se nalazimo u zadnjoj kategoriji i datum je stariji od pocetnog(odnosno stariji od 1.1.2020) dosli smo do kraja
                        if(zadnjiDate >= datumClanka and zadnjaKategorija == True):
                            print('-----------------------------------------------')
                            print('DOSLI SMO DO ZADNJEG CLANKA.')
                            print('Ukupan broj preuzetih clanaka: ', broj_sveukupno)
                            print('Kraj.')    
                            print('-----------------------------------------------')

                            log_file = open('log.txt', 'a', encoding= 'utf-8')
                            log_file.write('-----------------------------------------------\n')
                            log_file.write('DOSLI SMO DO ZADNJEG CLANKA.\n')
                            log_file.write('Ukupan broj preuzetih clanaka: ' + str(broj_sveukupno) + '\n')
                            log_file.write('Kraj\n')    
                            log_file.write('-----------------------------------------------\n')
                            log_file.close()

                            zadnjiClanak = True
                            break
                        

                        if(start >= datumClanka):
                            zadnjiClanakKategorija = True
                            print('-----------------------------------------------')
                            print('DOSLI SMO DO ZADNJEG CLANKA KATEGORIJE.')
                            print('Broj clanaka unutar kategorije: ', broj_clanakaKategorije)
                            print('Prelazimo na sljedeću kategoriju')    
                            print('-----------------------------------------------')
                            
                            log_file = open('log.txt', 'a', encoding= 'utf-8')
                            log_file.write('-----------------------------------------------\n')
                            log_file.write('DOSLI SMO DO ZADNJEG CLANKA KATEGORIJE.\n')
                            log_file.write('Broj clanaka unutar kategorije: ' + str(broj_clanakaKategorije) + '\n')
                            log_file.write('Prelazimo na sljedeću kategoriju...\n')    
                            log_file.write('-----------------------------------------------\n')
                            log_file.close()
                            
                            broj_clanakaKategorije = 0
                            broj_clanka = 0 
                            broj_stranice = 1

                            break


            kategorija = pom

            #provjera da li je zadnji clanak
            if(zadnjiClanak == True):
                break
            if(zadnjiClanakKategorija == True):
                zadnjiClanakKategorija=False
                break
        if(zadnjiClanak == True):
            #print('Kraj')
            break    
else:
    print('Dosli smo do kraja')

#Kraj timera
end_time = time.time()
print('\nTime spent: ', str(end_time-start_time))


