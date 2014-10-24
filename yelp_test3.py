from yelpapi import YelpAPI
import json 
import urllib2 
import sys
import re 
from bs4 import BeautifulSoup 
import pandas as pd 
#from collections import Counter 


#establish OAuth 
consumer_key='OXu1Vw-76AWTvNiMiwwa7Q'
consumer_secret='CFxnvXLPjtT4-dYBVA424bR31CQ'
token='rk7CFgX6rusXNsYyqvM3Lshe5T9DA0Jn'
token_secret='uymnoSDiHtDgpfaPht1dYcebBVI'
yelp_api=YelpAPI(consumer_key, consumer_secret, token, token_secret)

#set up the search criteria

webpage="http://zipcodedistanceapi.redline13.com/rest/InCd3nq7k2svDGft6694boOOhRhqnwy5UaiYyJ5SLynoeDSkJ1pVpeKG517sxGxs/city-zips.json/San%20Francisco/CA"
request=urllib2.Request(webpage)
try:
    fetch=urllib2.urlopen(request)
except urllib2.URLError:
    sys.exit()

content=fetch.read()
decoded=content.decode("ASCII","ignore")
toDict=json.loads(decoded,strict=False)
############################################################################
categories=["food","grocery","restaurant"]
district=toDict['zip_codes']
dictRest={}
offset=[20]
for j in district:
    for category in categories:
        for k in offset:
            search_results=yelp_api.search_query(term=category,location=j,offset=k,limit=20)
            list_Business=search_results["businesses"]
            if len(list_Business)<>0:
                for i in list_Business:
                    if i['location'].has_key('coordinate') and i.has_key('categories'):
                        busi_id=i['id']
                        if busi_id not in dictRest.keys():
                            busi_info={}
                            busi_info['name']=i['name']
                            busi_info['categories']=i['categories']
                            busi_info['rating']=i['rating']
                            busi_info['url']=i['url']
                            #busi_info['postal_code']=i['location']['postal_code']
                            busi_info['longitude']=i['location']['coordinate']['longitude']
                            busi_info['latitude']=i['location']['coordinate']['latitude']
                            dictRest[busi_id]=busi_info


print "------------------------------------------------------------------------"


for id in dictRest.keys():
    #print dictRest[id]['name']
    url=dictRest[id]['url']
    request=urllib2.Request(url)
    fetch=urllib2.urlopen(request)
    soup=BeautifulSoup(fetch.read())
    price_range=soup.find("dd", class_="nowrap price-description")
    if price_range is not None:
        dictRest[id]['price_range']=price_range.string.strip()
        operating_hours=[]
        operating_date=[]
        operating_schedule={}
        table=soup.find("table",{"class":"table table-simple hours-table"})
        try:
            rows=table.findAll("th",{"scope":"row"})
        except AttributeError:
            continue
        for row in rows:
            if row is not None:
                operating_date.append(row.string)
                #print row.string
                td=row.findNextSiblings()
                first_tag=td[0]
                children=first_tag.findChildren()
                #print children 
                if children is not None:
                    list_schedule=[]
                    for child in children:
                        list_schedule.append(child.text)
                    if len(list_schedule)==2:
                        dict_schedule={}
                        dict_schedule['opening']=list_schedule[0]
                        dict_schedule['closing']=list_schedule[1]
                        operating_hours.append([dict_schedule])
                    elif len(list_schedule)>2:
                        dict_schedule1={}
                        dict_schedule2={}
                        dict_schedule1['opening']=list_schedule[0]
                        dict_schedule1['closing']=list_schedule[1]
                        dict_schedule2['opening']=list_schedule[3]
                        dict_schedule2['closing']=list_schedule[4]
                        operating_hours.append([dict_schedule1,dict_schedule2])
                    else:
                        text_schedule=first_tag.text
                        text_schedule_strip_newline=re.sub(r'[\n|\s]*','',text_schedule)
                        dict_schedule={}
                        if text_schedule_strip_newline=="Closed":
                            dict_schedule['opening']="0:00 am"
                            dict_schedule['closing']="0:00 am"
                        else:
                            dict_schedule['opening']="0:00 am"
                            dict_schedule['closing']="11:59 pm"
                        operating_hours.append([dict_schedule])
                else:
                    del dictRest[id]
        for i in zip(operating_date,operating_hours):
            operating_schedule[i[0]]=i[1]
        dictRest[id]["operating_schedule"]=operating_schedule
        #print json.dumps(dictRest[id],indent=5)

with open('data_f.json', 'w') as outfile:
    json.dump(dictRest, outfile)



        
        





    
    
    


   


    
    





    

        
    
            
        

        
        
        
    



    
    
    






