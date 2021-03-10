import os
import csv
import pandas as pd
import warnings



#POSTAVKE ISPISA
#pd.set_option('display.max_rows',None)
pd.reset_option('display.max_rows')

#   I. Kvantificiranje clanaka u medijima
# Trazeni pojmovi

pojmovi = ['koron','mjere','covid','cjepivo','zaražen','virus','mjerama','slučajeva','slučaja','karanten']

print('-------------------------------------------------------')
print('\t\tANALIZA PODATAKA')
print('-------------------------------------------------------')

#Ucitavanje linkova - UKUPAN BROJ OBJAVA
def covid_table():
    df = pd.read_csv('rijekadanas.csv', encoding='utf-8', sep=',')
    nlinks = len(df)
    print('a) Ukupan broj objava na portalu za vremenski period 1.1.2020. - 30.11.2020. : ', nlinks)

    df['Published_date'] = df['Published_date'].astype('datetime64[ns]')
    df = df.sort_values(by=['Published_date'])

    #TRAZENJE KORONA POJMOVA: 
    warnings.filterwarnings("ignore", 'This pattern has match groups')
    df['Korona'] = df['Title'].str.contains(('(' + '|'.join(pojmovi) + ')'), case = False)
    #promjena iz boolean u int:
    df['Korona'] = df['Korona'].astype(int)

    df.to_csv('data_covid.csv', encoding='utf-8', index = False)

   
    print('b) Broj vijesti vezanih za korona tematiku: ', (df['Korona']==1).sum())


def covid_category():
    input= 'data_covid.csv'

    csv_reader = pd.read_csv(input, encoding='utf-8', sep= ',')
    df = pd.DataFrame(csv_reader, columns=['Category', 'Korona'])
    
    data_category = df.pivot_table(index = ['Category'], aggfunc = {'Category':len,'Korona':lambda x: (x>0).sum()})

    data_category.columns = ['All', 'Covid-19']
    data_category.index.name  = 'Category'

    category_order = ['Covid-19','All']
    data_category = data_category.reindex(columns = category_order)

    print('-------------------------------------------------------')
    print('\t\tCovid-19 articles by Category')
    print('-------------------------------------------------------')
    print(data_category)

    data_category.to_csv('data_category.csv', encoding= 'utf-8')

def covid_month():
    input= 'data_covid.csv'

    csv_reader = pd.read_csv(input, encoding='utf-8', sep= ',')
    df = pd.DataFrame(csv_reader, columns=['Published_date', 'Korona'])

    df['Month'] = pd.DatetimeIndex(df['Published_date']).month
    data_month = df.pivot_table(index = ['Month'], aggfunc = {'Month':len, 'Korona':lambda x: (x>0).sum()})

    data_month.columns = ['Covid-19','All']
    m = pd.Series(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sept', 'Oct','Nov'])
    data_month.set_index(m, inplace = True)
    data_month.index.name = 'Month'

    print('-------------------------------------------------------')
    print('\t\tCovid articles by Month')
    print('-------------------------------------------------------')
    print(data_month)
    data_month.to_csv('data_month.csv',encoding = 'utf-8')
def covid_day():
    input= 'data_covid.csv'

    csv_reader = pd.read_csv(input, encoding='utf-8', sep= ',')
    df = pd.DataFrame(csv_reader, columns=['Published_date', 'Korona']) 

    data_day = df.pivot_table(index = ['Published_date'], aggfunc = {'Published_date':len, 'Korona':lambda x: (x>0).sum()})

    data_day.columns = ['Covid-19','All']
    data_day.index.name = 'Date' 

    print('-------------------------------------------------------')
    print('\t\tCovid articles by Day')
    print('-------------------------------------------------------')
    print(data_day)
    data_day.to_csv('data_day.csv',encoding = 'utf-8')     


def delete_file(path):
    if os.path.exists(path):
        os.remove(path)


#--------------------------------------------------------------------------------------Main-------------------------------------------------------------------------------------------

delete_file('data_covid.csv')
delete_file('data_category.csv')
delete_file('data_month.csv')
delete_file('data_day.csv')

covid_table()
covid_category()
covid_month()
covid_day()