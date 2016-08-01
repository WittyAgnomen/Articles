#http://newspaper.readthedocs.io/en/latest/user_guide/install.html#install
#leverages library: newspaper
#get articles, version 0.1
#use np enviroment (np-env)

#import newspaper someone should explore this more
import xml.etree.ElementTree as ET
import pandas as pd
import random
import urllib2

#http://feeds.foxnews.com/foxnews/politics
#http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml

#create stucture/table to hold data
data = pd.DataFrame([['test','test']], columns=['url','leaning'])

#holds rss/xml pages, will add more
papers=['http://feeds.foxnews.com/foxnews/politics','http://rss.nytimes.com/services/xml/rss/nyt/Politics.xml']

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
				arr=['dl parser error']
				count+=1
		
			#pd.Series(arr)
			#add to dataframe
			data.loc[len(data)]=arr

	except:
		print 'error with loading site'

data.to_csv('urlfeed.csv') #save a csv






