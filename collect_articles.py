#http://newspaper.readthedocs.io/en/latest/user_guide/install.html#install
#leverages library: newspaper
#get articles, version 0.1
#use np enviroment (np-env)

#import newspaper someone should explore this more
import xml.etree.ElementTree as ET
import pandas as pd
import random
import urllib2
import sqlite3

#http://feeds.foxnews.com/foxnews/politics
#http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml

#create stucture/table to hold data
#data = pd.DataFrame([['test','test']], columns=['url','leaning'])

#connect to sql database
conn = sqlite3.connect('articles.db')

#create cursor
c = conn.cursor()

#holds rss/xml pages, will add more
papers=['http://feeds.foxnews.com/foxnews/politics','http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml',
	'http://rss.cnn.com/rss/cnn_allpolitics.rss',
	'http://www.huffingtonpost.com/feeds/verticals/politics/news.xml',
	'http://feeds.slate.com/slate-101526',
	'http://www.politico.com/rss/politics08.xml',
	'http://www.wnd.com/category/front-page/politics/feed/',
	'http://www.theblaze.com/stories/feed/'
	]

#loop for going through each xml
for p in papers:
	try:
		request = urllib2.Request(p) 
		article = urllib2.urlopen(request)
		
		e = ET.parse(article) #load xml using ET
		count=0 #for counting total articles added
		
		#move down tree to lower node
		channel=e.find('channel')

		#to show user what feed we are working on, and if there is any errors
		print '=========================================================='
		print 'Working on ' + p
		print '=========================================================='

		for item in channel.iter('item'):
			try:

				print 'working on article ' +str(count)
				arr=[]
			
				try:
					arr.append(item.find('guid').text) #get url
				except:
					arr.append('url error')

				try:
					arr.append(('left' if random.randint(0,1)==1 else 'right')) #return left or right randomly
				except:
					arr.append('leaning error')
			
				count+=1
			
			except:
				arr=['dl parser error','']
				count+=1
		
			#pd.Series(arr)
			#add to dataframe
			#data.loc[len(data)]=arr
			
			#add row to sql, add only unique articles later
			c.execute('INSERT INTO articles VALUES (?,?)', arr)

	except:
		print 'error with loading site'

# Save (commit) the changes
conn.commit()

#close sqlite connection
conn.close()


#data.to_csv('urlfeed.csv') #save a csv

#update table to only take unique
'''
sqlite> create table articles
   ...> (
   ...> url varchar(2048) not null unique,
   ...> leaning varchar(8)
   ...> );
'''





