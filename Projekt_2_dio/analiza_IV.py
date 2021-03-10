#Dodatna analiza 
import os
import pandas as pd                 
import csv   
import numpy as np
import matplotlib.pyplot as plt

pd.options.mode.chained_assignment = None  # default='warn'
#Vidjeti koji su top 20 najgledanijih objava, te da li su oni vezani uz koronu ili nisu
def most_viewed_articles(top_number):

    input_csv = 'data_covid.csv'
    output_csv = 'aditional/most_view_covid.csv'

    df = pd.read_csv(input_csv)

    #df = df[df['Korona'] == 1]
    df = df.drop(df.index[[0]])
    del df['ID']
    df = df.reset_index()
    df = df[['Title', 'Views','Korona']]

    #df.insert(0, 'ID', range(1, 1 + len(df)))
    df = df.sort_values("Views", ascending = False)
    
    df = df.head(top_number)
    df.to_csv(output_csv, encoding = 'utf-8', index = False)

def graph_views():
    
    input_csv = 'aditional/most_view_covid.csv'
    df = pd.read_csv(input_csv)

    print('-----------------------------------------------------------------------------')
    print('\t\tTop 20 najgledanijih objava: ')
    print('-----------------------------------------------------------------------------')

    print(df)
    print('\nOd ' +str(len(df)) + ' najgledanijih objava ' + str((df['Korona']==1).sum()) + ' ih je bilo korona tematike')

    df_korona = df[df['Korona'] == 1]
    leng = len(df_korona) + 1
    df_korona['Title'] = np.arange(1,leng)

    df_nokorona = df[df['Korona'] == 0]
    leng1 = len(df_nokorona) + 1
    df_nokorona['Title'] = np.arange(1,leng1)

    # Line plot

    # Korona data
    x1 = df_korona['Title']
    y1 = df_korona['Views']
    plt.plot(x1, y1, label = "Korona Views")

    # No Korona data
    x2 = df_nokorona['Title']
    y2 = df_nokorona['Views']
    plt.plot(x2, y2, label = "No Korona Views")


    plt.xlabel('Articles')
    plt.ylabel('Views')
    plt.title('Top 20 most viewed articles')
    plt.legend()

    plt.savefig('aditional/areaplot_views.png')


    # Omjer views-a 
    #Zbroj korona pogleda, i ne korona pogleda, zatim prikaz u pie-chartu

    df_korona_num = df_korona['Views'].sum()
    df_nokorona_num = df_nokorona['Views'].sum()

    labels = ['Korona Views', 'No Korona Views']
    sizes = [df_korona_num, df_nokorona_num]
    fig = plt.figure()
    ax = plt.subplot()
    ax.set_title('Top '+str(len(df)) +' most viewed articles - by percentage')
    ax.pie(sizes, labels=labels, autopct = '%1.1f%%', startangle = 90)
    ax.legend(sizes, loc = 'lower right')
    ax.axis('equal')

    plt.savefig('aditional/pieplot_views.png')

def graph_views_more():
    input_csv = 'aditional/most_view_covid.csv'
    df = pd.read_csv(input_csv)


    print('\nOd ' + str(len(df)) + ' najgledanijih objava ' + str((df['Korona']==1).sum()) + ' ih je bilo korona tematike')

    df_korona = df[df['Korona'] == 1]
    leng = len(df_korona) + 1
    df_korona['Title'] = np.arange(1,leng)

    df_nokorona = df[df['Korona'] == 0]
    leng1 = len(df_nokorona) + 1
    df_nokorona['Title'] = np.arange(1,leng1)

    df_korona_num = df_korona['Views'].sum()
    df_nokorona_num = df_nokorona['Views'].sum()

    labels = ['Korona Views', 'No Korona Views']
    sizes = [df_korona_num, df_nokorona_num]
    fig = plt.figure()
    ax = plt.subplot()
    ax.set_title('Top '+str(len(df)) +' most viewed articles - by percentage')
    ax.pie(sizes, labels=labels, autopct = '%1.1f%%', startangle = 90)
    ax.legend(sizes, loc = 'lower right')
    ax.axis('equal')

    plt.savefig('aditional/pieplot_views_more.png')

#--------------------------------------------------------------------------------------Main-------------------------------------------------------------------------------------------

most_viewed_articles(20)
graph_views()

most_viewed_articles(100)
graph_views_more()

