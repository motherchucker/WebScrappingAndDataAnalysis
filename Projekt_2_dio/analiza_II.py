import os 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

pd.options.mode.chained_assignment = None  # default='warn'

data_day = pd.read_csv('data_day.csv', encoding= 'utf-8', sep= ',')
data_month = pd.read_csv('data_month.csv', encoding= 'utf-8', sep= ',')
data_category = pd.read_csv('data_category.csv', encoding= 'utf-8', sep= ',')

data_day = pd.DataFrame(data_day)
data_month = pd.DataFrame(data_month)
data_category = pd.DataFrame(data_category)


#--------------------------------------------------------------------------------------Day plots-------------------------------------------------------------------------------------------

# Area plot
data_day.plot.area(title = 'Number of all articles and Covid-19 related ones by date',x = 'Date', y=['All','Covid-19'], stacked = False,figsize =(10,6), colormap = 'Accent', ylabel ='Number of articles')
plt.savefig('graph/day_areaplot.png')


# Plot - line - max value
sub_data_day = data_day.copy()
sub_data_day['Date'] = pd.to_datetime(sub_data_day['Date'])
sub_data_day = sub_data_day.set_index(sub_data_day['Date'])
sub_data_day = sub_data_day.sort_index()
sub_data_day = sub_data_day['2020-3-1':'2020-5-28'] 
sub_data_day['Date'] = pd.to_datetime(sub_data_day['Date']).dt.date

fig = plt.figure(figsize= (10,6))
ax = fig.add_subplot(111)
x = sub_data_day['Date']
y = sub_data_day['Covid-19']

line, = ax.plot(x,y)
ymax = max(y)
xmax = x[np.argmax(y)]
ax.annotate ('Max number of Covid-19 articles: {0} \nwere on date: {1}'.format(ymax,xmax), xy= (xmax,ymax), xytext=(xmax,ymax+5), arrowprops = dict(facecolor = 'black', shrink=0.05),)
ax.set_ylim(0,20)
ax.set_title('Spring period - period of max number of Covid-19 articles')
ax.set_xlabel('Date')
ax.set_ylabel('Number of articles')
plt.savefig('graph/day_lineplot.png')


#--------------------------------------------------------------------------------------Month plots-------------------------------------------------------------------------------------------

# Bar plot
data_month.plot.bar(title = 'Number of all articles and Covid-19 related ones',x = 'Month', y=['All','Covid-19'], figsize =(10,6), colormap = 'coolwarm', ylabel ='Number of articles')
plt.savefig('graph/month_barplot.png')


fig = plt.figure()
data_month['Other']=data_month['All']-data_month['Covid-19']
data_month = data_month.drop(columns=['All'])
data_month = data_month.iloc[::-1]


data_month.plot.barh (title = 'Percentage of Covid-19 related articles and others',x = 'Month', stacked = True,figsize =(10,7), colormap = 'Pastel1', ylabel ='Number of articles', xlabel = '', mark_right = True, xlim = (-25,500))

data_total = data_month['Other'] + data_month['Covid-19'] 
data_rel = data_month[data_month.columns[1:]].div(data_total,0)*100

for n in data_rel:
    for i, (cs, ab, pc) in enumerate(zip(data_month.iloc[:, 1:].cumsum(1)[n],  
                                         data_month[n], data_rel[n])): 
        plt.text(cs - ab / 2, i, str(np.round(pc, 1)) + '%',  
                 va = 'center', ha = 'center')

plt.savefig('graph/month_barhplot.png')

#--------------------------------------------------------------------------------------Category plots-------------------------------------------------------------------------------------------

# (1,2) Pie plot
labels = ['Biznis','Kolumne','Mozaik','Najnovije','Sport','Vijesti']
fig = plt.figure()
ax1 = fig.add_subplot(121)
ax2 = fig.add_subplot(122)

data_category.plot(kind = 'pie', ax = ax1, y='All',figsize =(10,6), colormap = 'Spectral',title = 'Articles by Category', autopct ='%1.1f%%',  explode = (0.01,0.01,0.01,0.01,0.01,0.1),labels = ['','','','','',''])
data_category.plot(kind = 'pie', ax = ax2, y='Covid-19',figsize =(10,6), colormap = 'Spectral',title = 'Covid articles by Category', autopct ='%1.1f%%',  explode = (0.01,0.01,0.01,0.01,0.01,0.1),labels = ['','','','','',''], legend = False)
ax1.legend(loc='lower right',bbox_to_anchor=(1.27,0), labels=labels)
#plt.legend(loc='lower right', bbox_to_anchor=(1.3,0))

plt.savefig('graph/category_pieplot.png')

#Vijesti nisu relevantne posto su ocigledno najvece, pa cemo pogledati kako izgleda graf bez njih,sortirane po covid-u
fig = plt.figure()
data_category_bez = data_category[:-1]
data_category_bez = data_category_bez.sort_values(by=['Covid-19'])
data_category_bez.plot.bar(title = 'Number of all articles and Covid-19 related ones by category - without Vijesti',x = 'Category', y=['All','Covid-19'], stacked = False,figsize =(10,7), colormap = 'cividis', ylabel ='Number of articles', xlabel = 'Category')

plt.savefig('graph/category_barplot_bez_vijesti.png')

#Kod vijesti pak zelimo prikazati omjer covid vijesti i normalnih
fig = plt.figure()
data_category_vijesti= data_category.tail(1)
data_category_vijesti['Other']=data_category_vijesti['All']-data_category_vijesti['Covid-19']
data_category_vijesti = data_category_vijesti.drop(columns=['All'])

data_category_vijesti.plot.barh(title = 'Number of all articles and Covid-19 related in column Vijesti',x = 'Category', y=['Covid-19','Other'], stacked = True,figsize =(10,7), colormap = 'tab20', ylabel ='Number of articles', xlabel = '', mark_right = True)
data_total = data_category_vijesti['Other'] + data_category_vijesti['Covid-19'] 
data_rel = data_category_vijesti[data_category_vijesti.columns[1:]].div(data_total,0)*100

for n in data_rel:
    for i, (cs, ab, pc) in enumerate(zip(data_category_vijesti.iloc[:, 1:].cumsum(1)[n],  
                                         data_category_vijesti[n], data_rel[n])): 
        plt.text(cs - ab / 2, i, str(np.round(pc, 1)) + '%',  
                 va = 'center', ha = 'center')

plt.savefig('graph/category_barhplot_vijesti.png')

