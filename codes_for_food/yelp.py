from yelpapi import YelpAPI
import json 
import urllib2 
import sys
import re 
from bs4 import BeautifulSoup 
from pandas import * 



def get_zip_codes(webpage):
    
    request = urllib2.Request(webpage)
    try:
        fetch = urllib2.urlopen(request)
    except urllib2.URLError:
        sys.exit()

    content = fetch.read()
    decoded = content.decode("ASCII","ignore")
    toDict = json.loads(decoded, strict = False)
    
    return toDict["zip_codes"]





def get_info_from_api(consumer_key, consumer_secret, token, token_secret, district, categories):
    
    yelp_api = YelpAPI(consumer_key, consumer_secret, token, token_secret)

    dictRest = {}
    
    offset = [0]

    for j in district:
        for category in categories:
            for k in offset:
                search_results=yelp_api.search_query(term = category,location = j,offset = k,limit = 20)
                list_Business=search_results["businesses"]
                if len(list_Business) <> 0:
                    for i in list_Business:
                        if i["location"].has_key("coordinate") and i.has_key("categories"):
                            busi_id=i["id"]
                            if busi_id not in dictRest.keys():
                                busi_info = {}
                                busi_info["name"] = i["name"]
                                busi_info["categories"] = i["categories"]
                                busi_info["rating"] = i["rating"]
                                busi_info["url"] = i["url"]
                                busi_info["longitude"] = i["location"]["coordinate"]["longitude"]
                                busi_info["latitude"] = i["location"]["coordinate"]["latitude"]
                                dictRest[busi_id] = busi_info

    return dictRest





def get_info_from_webscraping(dictRest, filename):

    for id in dictRest:
        url=dictRest[id]["url"]
        request=urllib2.Request(url)
        fetch=urllib2.urlopen(request)
        soup=BeautifulSoup(fetch.read())
        price_range=soup.find("dd", class_="nowrap price-description")
        if price_range is not None:
            dictRest[id]["price_range"]=price_range.string.strip()
            operating_hours=[]
            operating_date=[]
            operating_schedule={}
            table=soup.find("table", {"class":"table table-simple hours-table"})
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
                        if len(list_schedule) == 2:
                            dict_schedule = {}
                            dict_schedule["opening"] = list_schedule[0]
                            dict_schedule["closing"] = list_schedule[1]
                            operating_hours.append([dict_schedule])
                        elif len(list_schedule) > 2:
                            dict_schedule1 = {}
                            dict_schedule2 = {}
                            dict_schedule1["opening"] = list_schedule[0]
                            dict_schedule1["closing"] = list_schedule[1]
                            dict_schedule2["opening"] = list_schedule[3]
                            dict_schedule2["closing"] = list_schedule[4]
                            operating_hours.append([dict_schedule1,dict_schedule2])
                        else:
                            text_schedule = first_tag.text
                            text_schedule_strip_newline = re.sub(r"[\n|\s]*","",text_schedule)
                            dict_schedule = {}
                            if text_schedule_strip_newline == "Closed":
                                dict_schedule["opening"] = "0:00 am"
                                dict_schedule["closing"] = "0:00 am"
                            else:
                                dict_schedule["opening"] = "0:00 am"
                                dict_schedule["closing"] = "11:59 pm"
                            operating_hours.append([dict_schedule])
                    else:
                        del dictRest[id]
        for i in zip(operating_date,operating_hours):
            operating_schedule[i[0]] = i[1]
        dictRest[id]["operating_schedule"] = operating_schedule
        
        
    with open(filename, "w") as outfile:
        json.dump(dictRest, outfile)






def generate_csv(filename, days):

    openFile = open(filename, "r")
    content = openFile.readlines()
    jsonfile = json.loads(content[0])
    
    for day in days:
        giant_list = []
        for i in jsonfile:
            small_dict = {}
            small_dict["id"] = i 
            small_dict["latitude"] = jsonfile[i]["latitude"]
            small_dict["longitude"] = jsonfile[i]["longitude"]
            if jsonfile[i].has_key("operating_schedule"):
                if len(jsonfile[i]["operating_schedule"][day]) == 2:
                    small_dict["opening_1"] = jsonfile[i]["operating_schedule"][day][0]["opening"]
                    small_dict["closing_1"] = jsonfile[i]["operating_schedule"][day][0]["closing"]
                    small_dict["opening_2"] = jsonfile[i]["operating_schedule"][day][1]["opening"]
                    small_dict["closing_2"] = jsonfile[i]["operating_schedule"][day][1]["closing"]
                else:
                    small_dict["opening_1"] = jsonfile[i]["operating_schedule"][day][0]["opening"]
                    small_dict["closing_1"] = jsonfile[i]["operating_schedule"][day][0]["closing"]
                    small_dict["opening_2"] = 0
                    small_dict["closing_2"] = 0 
            giant_list.append(small_dict)
        df = DataFrame(giant_list)
        df.to_csv("operating_hours_" + day + ".csv", sep = ",")






if __name__ == "__main__":

    # webpage containing San Francisco zip codes 
    zip_page = "http://zipcodedistanceapi.redline13.com/rest/InCd3nq7k2svDGft6694boOOhRhqnwy5UaiYyJ5SLynoeDSkJ1pVpeKG517sxGxs/city-zips.json/San%20Francisco/CA"
    
    # info to establish OAuth 
    yelp_consumer_key = "DZXDgT4C71lx7gTI3KdX5A"
    yelp_consumer_secret = "FsCCaeIY5L2kaVj3K26dQPsSmYA"
    yelp_token = "2CIuq-KubVw5URBKzwlWz7xYfgDADXPk"
    yelp_token_secret = "4nxRhTnj_gfhPYVa6IVBCwhQKMw"


    search_category = ["food","grocery","restaurant"]
    

    sf_zip_codes = get_zip_codes(zip_page)

    api_info = get_info_from_api(yelp_consumer_key, yelp_consumer_secret, yelp_token, yelp_token_secret, sf_zip_codes, search_category)
    
    get_info_from_webscraping(api_info, "data.txt")

    generate_csv("data.txt", ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"])
    
   




