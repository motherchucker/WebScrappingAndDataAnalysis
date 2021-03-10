import os
import pandas as pd                 
import csv   
import numpy as np     
import nltk
#nltk.download('punkt')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from datetime import datetime
import dateutil.parser
from wordcloud import WordCloud 
import matplotlib.pyplot as plt 
from PIL import Image
import heapq
import matplotlib.image as mpimg 
from matplotlib.offsetbox import TextArea, DrawingArea, OffsetImage, AnnotationBbox
             

def delete_file(path):
    if os.path.exists(path):
        os.remove(path)

def covid_articles():
    delete_file('covid_articles.csv')

    input_csv = 'data_covid.csv'
    output_csv = 'only_covid_data.csv'

    df = pd.read_csv(input_csv)

    #Samo redovi u kojima ima korona tematike, odnosno di je Korona = 1 
    df = df[df['Korona'] == 1]
    
    #df.replace(r'^\s+$', np.nan, regex=True)  #Zamjena space-a u nan
    #Tags stupac ima NaN vrijednosti, potrebno ih je promijeniti u string
    #U suprotnom svaki stupac u kojem je Tags NaN kod spajana bude prazan
    df = df.replace(np.nan, '',regex = True)

    #Spajanje stupaca
    df['Text_All'] = df['Title'] + ' ' + df['Text'] + ' ' + df['Tags']
    df['Text_All'] = df['Text_All'].str.lower()
    #Micanje svih tocka u tekstu. Iako se tocka nalazi u .txt datoteci sa stopword-ima, kod slucajeva kao sto su 24. ili dnevnik.hr word_freq() uzima tu tocku kao posebnu rijec.
    df['Text_All'] = df['Text_All'].replace(r'\.', '', regex = True)

    #Manualno brisanje prvog reda jer nema veze s koronom:
    df = df.drop(df.index[[0]])

    #Za nastavak analize trebat ce nam spojeni tekst i datumi kako bismo mogli raspodjelit kasnije po mjesecima
    df = df[['Published_date', 'Text_All']]
    df.index.name = 'ID'
    
    df.to_csv(output_csv, encoding = 'utf-8')

def txt_to_list(input_txt):
    words_list = []
    txt = open(input_txt, 'r', encoding= 'utf-8')

    for row in txt:
        row = row.rstrip()
        words_list.append(row)
    return words_list

def covid_without_stopwords():
    delete_file('data/final_covid_data.csv')

    stop_words = []
    
    stop_words_txt = txt_to_list('data/ocistiti.txt')


    for i in stop_words_txt: 
        if i not in stop_words: 
            stop_words.append(i) 
    #print(stop_words)

    input_csv = 'only_covid_data.csv'
    output_csv = 'data/final_covid_data.csv'

    ID = 0

    with open(input_csv, 'r', encoding= 'utf-8') as read_csv, \
        open(output_csv, 'a', encoding= 'utf-8') as write_csv:

        read_csv = csv.reader(read_csv, delimiter = ',')
        write_csv = csv.writer(write_csv, delimiter = ',', quotechar= '"', quoting = csv.QUOTE_MINIMAL, lineterminator = '\n')
        headers = ['ID', 'Date', 'Text']

        write_csv.writerow(headers)
        next(read_csv, None)

        for row in read_csv:
            row[2] = row[2].lstrip('"')
            word_tokens = word_tokenize(row[2])
            filtered_row = []

            for word in word_tokens:
                if word not in stop_words:
                    filtered_row.append(word)

            ID += 1
            filtered_text = (' ').join(filtered_row)

            write_csv.writerow([ID, row[1], filtered_text])

def month(x):
    return(x.month)

#Razdvajanje df na df po mjesecu
def get_months(month_number):
    input_csv = ('data/final_covid_data.csv')
    output_csv = ('data/months/covid_data_month_' + str(month_number) + '.csv')
    df = pd.read_csv(input_csv, encoding= 'utf-8', sep= ',')
    df.reset_index()
    df.Date = df.Date.apply(dateutil.parser.parse)
    df['Month'] = df.Date.apply(month)

    df = df[(df['Month'] == month_number)]
    del df['Month']

    df.to_csv(output_csv, mode = 'w', encoding = 'utf-8', sep = ',', index = False)

#Trazenje najcescih rijeci unutar clanaka po mjesecu
def word_freq(month_number):
    input_csv = ('data/months/covid_data_month_'+ str(month_number) + '.csv')
    output_csv = ('data/word_freq_' + str(month_number) + '.csv')

    df = pd.read_csv(input_csv, encoding= 'utf-8', sep= ',')
    del df['ID']

    word = df['Text'].str.lower().str.cat(sep= ' ')
    words = nltk.tokenize.word_tokenize(word)
    words_dist = nltk.FreqDist(words)

    df_months = pd.DataFrame(words_dist.most_common(25), columns= ['Word','Frequency'])

    df_months['Month'] = month_number
    df_months.index.name = 'ID'
    df_months = df_months[['Month', 'Word', 'Frequency']]

    print('\n', df_months)

    df_months.to_csv(output_csv, mode = 'w', encoding = 'utf-8', sep = ',')

#Graficki prikaz uz pomoc WordCloud-a
def word_plot(month_number):
    input_csv = ('data/word_freq_' + str(month_number) + '.csv')
    output_png = ('graph/word_freq_' + str(month_number) + '.png')

    df = pd.read_csv(input_csv, encoding= 'utf-8', sep= ',')
    text = ' '.join(word for word in df.Word)

    #Load image
    wave_mask = np.array(Image.open( "K.jpg"))
    
    wordcloud = WordCloud(mask=wave_mask, colormap= 'Blues').generate(text)
    plt.figure()
    plt.title('Most frequent words in ' + str(month_number) + ' :')
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.margins(x=0, y=0)
    #plt.show()

    wordcloud.to_file(output_png)

#Jaccard indeks
def jaccard_index(list1, list2):

    intersection = len(list(set(list1).intersection(list2)))
    union = (len(list1) + len(list2)) - intersection
    
    result = float(intersection) / union
    result = round(result, 2)

    return result

def jaccard(month_1, month_2):
    freq_data_1 = 'data/word_freq_' + str(month_1) + '.csv'
    freq_data_2 = 'data/word_freq_' + str(month_2) + '.csv'

    output_csv = 'data/jaccard_index.csv'

    df_1 = pd.read_csv(freq_data_1, encoding = 'utf-8', sep = ',')
    df_2 = pd.read_csv(freq_data_2, encoding = 'utf-8', sep = ',')

    list_1 = list(df_1['Word'])
    list_2 = list(df_2['Word'])

    print('Jaccard index for '+ str(month_1) + '. and ' + str(month_2) + '. month')
    jaccard = jaccard_index(list_1, list_2)
    print(jaccard)

    with open(output_csv, 'a', encoding = 'utf-8') as output_file:

        csv_writer = csv.writer(output_file, delimiter=',', lineterminator = '\n')
        months = str(month_1) + '-' + str(month_2)
        row = [months, jaccard]

        if(os.stat(output_csv).st_size == 0):
            headers = ['Months', 'Jaccard_index']
            csv_writer.writerow(headers)
            csv_writer.writerow(row)
        else:
            csv_writer.writerow(row)

#Graficki prikaz jaccard-ovog indeksa
def jaccard_plot():
    input_csv = 'data/jaccard_index.csv'

    df = pd.read_csv(input_csv, encoding= 'utf-8', sep= ',')


    fig = plt.figure(figsize= (10,6))
    ax = fig.add_subplot(111)
    x = df['Months']
    y = df['Jaccard_index']
   
    line, = ax.plot(x,y)
    ymax = max(y)
    xmax = x[np.argmax(y)]

    ymax2 = sorted(y)[-2] 
    xmax2 = x[9]
    
    ax.annotate ('Highest Jaccard \nindex: {0} \nwas in: {1}'.format(ymax,xmax), xy= (xmax,ymax), xytext=(xmax,ymax+0.25), arrowprops = dict(facecolor = 'black', shrink=0.05),)
    ax.annotate ('2nd highest Jaccard \nindex: {0} \nwas in: {1}'.format(ymax2,xmax2), xy= (xmax2,ymax2), xytext=(xmax2,ymax2+0.25), arrowprops = dict(facecolor = 'black', shrink=0.05),)
    ax.set_ylim(0,1.2)
    ax.set_xlim(0,11)
    
    question = mpimg.imread('slike/question.png')
    imagebox = OffsetImage(question, zoom = 0.2)
    ab = AnnotationBbox(imagebox, (9.7,0.3))
    
    ax.add_artist(ab)
    
    ax.set_title('Jaccard index by months')
    ax.set_xlabel('Months')
    ax.set_ylabel('Jaccard index')
    plt.savefig('graph/jaccard_index.png')
#--------------------------------------------------------------------------------------Main-------------------------------------------------------------------------------------------
covid_articles()
covid_without_stopwords()

for i in range (1,12):
    get_months(i)


#Prikaz frekvencija tablicno
for i in range(1,12):
    word_freq(i)

for i in range(1,12):
    word_plot(i)

delete_file('data/jaccard_index.csv')

for i in range(1,11):
    if(i == 11):
        jaccard(i,1)
    else:
        jaccard(i,i+1)

jaccard_plot()