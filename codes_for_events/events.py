# this code creates json file for given dates
import csv
import md5
import urllib
import httplib2
import simplejson
import re
import json
import random
import codecs
import sys

reload(sys);
sys.setdefaultencoding("utf8")

zip_codes=["94101","94102","94103","94104","94105","94106","94107","94108","94109","94110","94111","94112","94114",
"94115","94116","94117","94118","94119","94120","94121","94122","94123","94124","94125","94126","94127","94128","94129",
"94130","94131","94132","94133","94134","94135","94136","94137","94138","94139","94140","94141","94142","94143","94144",
"94145","94146","94147","94150","94151","94152","94153","94154","94155","94156","94158","94159","94160","94161","94162",
"94163","94164","94171","94172","94175","94177","94188","94199"]

__all__ = ['APIError', 'API']

class APIError(Exception):
    pass

class API:
    def __init__(self, app_key, server='api.eventful.com', cache=None):
        """Create a new Eventful API client instance.
If you don't have an application key, you can request one:
    http://api.eventful.com/keys/"""
        self.app_key = app_key
        self.server = server
        self.http = httplib2.Http(cache)

def getUrl(api, method, **args):
    "Call the Eventful API's METHOD with ARGS."
    # Build up the request
    args['app_key'] = api.app_key
    if hasattr(api, 'user_key'):
        args['user'] = api.user
        args['user_key'] = api.user_key
    args = urllib.urlencode(args)
    url = "http://%s/json/%s?%s" % (api.server, method, args)
    api.url=url
    api.args=args
    
def makeRequest(url,method):
        # Make the request
    response, content = api.http.request(url, "GET")
    
    # Handle the response
    status = int(response['status'])
    if status == 200:
        try:
            return simplejson.loads(content)
        except ValueError:
            raise APIError("Unable to parse API response!")
    elif status == 404:
        raise APIError("Method not found: %s" % method)
    else:
        raise APIError("Non-200 HTTP response status: %s" % response['status'])
        
def getFeatures(elt):
    tempDict={}
    if not (elt.has_key("latitude") and elt.has_key("longitude")
    and elt.has_key("venue_id") and (elt["start_time"] is not None) ):
        return tempDict
    tempDict["latitude"]=elt["latitude"]
    tempDict["longitude"]=elt["longitude"]
    tempDict["venue_id"]=elt["venue_id"]
    tempDict["start_time"]=elt["start_time"]
    tempDict["stop_time"]=None
    if elt.has_key("id"):
        tempDict["id"]=elt["id"]
    if elt.has_key("venue_name"):
        tempDict["venue_name"]=elt["venue_name"]
    if elt.has_key("url"):
        tempDict["url"]=elt["url"]
    if elt.has_key("title"):
        tempDict["title"]=elt["title"]
    return tempDict
    
def getEvents(api,method,category,searchTerm,myDate,zip_codes):
    numberOfEvents=0
    # {event id1:{},...}
    myEvents={}
    for zipp in zip_codes:
        getUrl(api,method, c=category,q=searchTerm,t=myDate,l=zipp,page_size=200)
        myEvent=makeRequest(api.url,method)
        if not myEvent.has_key("events"):
            #print 1
            continue
        if (myEvent["events"] is None  or (not myEvent["events"].has_key("event"))):
            #print 2
            continue
        #print type(myEvent["events"]["event"])
        if type(myEvent["events"]["event"])==list:
            #print "length is", len((myEvent["events"]["event"]))
            numberOfEvents+=len((myEvent["events"]["event"]))
            for elt in myEvent["events"]["event"]:
                elt=getFeatures(elt)
                myEvents[elt["id"]]=elt         
        else:
            numberOfEvents+=1
            elt=myEvent["events"]["event"]
            elt=getFeatures(elt)
            myEvents[elt["id"]]=elt   
    return myEvents 
    
def reshapeEventsDict(myEvents):
    venues={}  
    for myEvent in myEvents:
        myEvent=myEvents[myEvent]
        venue_id=myEvent["venue_id"]
        event_id=myEvent["id"]
        start_time=re.sub(r'(.*\s)', '',myEvent["start_time"])
    
        if venues.has_key(venue_id):
            venues[venue_id]['events'][event_id]={}
            venues[venue_id]['events'][event_id]['start_time']=start_time
            venues[venue_id]['events'][event_id]['stop_time']=None
            venues[venue_id]['events'][event_id]['type']=category
            if myEvent.has_key('title'):
                venues[venue_id]['events'][event_id]['title']=myEvent['title']
            if myEvent.has_key('url'):
                venues[venue_id]['events'][event_id]['url']=myEvent['url']
            continue
        else:
            venues[venue_id]={}
            venues[venue_id]['latitude']=myEvent['latitude']
            venues[venue_id]['longitude']=myEvent['longitude']
            if  myEvent.has_key('venue_name'):
                venues[venue_id]['venue_name']=myEvent['venue_name']
            
            venues[venue_id]['events']={}
            venues[venue_id]['events'][event_id]={}
            venues[venue_id]['events'][event_id]['start_time']=start_time
            venues[venue_id]['events'][event_id]['stop_time']=None
            venues[venue_id]['events'][event_id]['type']=category
            if myEvent.has_key('title'):
                venues[venue_id]['events'][event_id]['title']=myEvent['title']
            if myEvent.has_key('url'):
                venues[venue_id]['events'][event_id]['url']=myEvent['url']
    return venues
def NumberOfEvents(Events):
    a=0
    for elt1 in Events:
        for elt2 in Events[elt1]:
            a+=len(Events[elt1][elt2]["events"])
    return a

def getVenueLocations(Events):
    venues={}
    for elt1 in Events:
        for elt2 in Events[elt1]:
            venues[elt2]={}
            venues[elt2]['venue_name']=Events[elt1][elt2]['venue_name']
            venues[elt2]['venue_id']=elt2
            venues[elt2]['latitude']=Events[elt1][elt2]['latitude']
            venues[elt2]['longitude']=Events[elt1][elt2]['longitude']
    return venues
def encode(companiesDict, fileName):
    with open(fileName, 'wb') as out_file:
            json.dump(companiesDict, out_file)
            
def decode(fileName):

    with open(fileName, 'rb') as in_file:
        Events = json.load(in_file)
    return Events

      
api = API('LPmMt8m8MncTtxbb')
method='/events/search'
#searchTerm="tag:classical"
searchTerm=""
category="music"
myDates=["2014-09-28","2014-09-29","2014-09-30"]
create_json=False
if create_json:
    Events={}
    for myDate in myDates:
        myEvents=getEvents(api,method,category,searchTerm,myDate,zip_codes)
        Events[myDate]=reshapeEventsDict(myEvents)
        encode(Events, 'Events.json')
else:
    Events = decode('Events.json')
    
numberOfEvents=NumberOfEvents(Events)
venues=getVenueLocations(Events)
len(venues)
type(venues)
venues['V0-001-000439892-0']


#create list of 10 venues
venueExamples=[["venue_id",'latitude',"longitude","weight","venue_name"]]
for i in range(10):
    name=venues.values()[i]['venue_name']
    idd=venues.values()[i]["venue_id"]
    latitude=venues.values()[i]['latitude']
    longitude=venues.values()[i]["longitude"]
    venueExamples.append([idd,latitude,longitude,random.random(),name])
import csv, StringIO
class UnicodeWriter(object):
    """
    Like UnicodeDictWriter, but takes lists rather than dictionaries.
    
    Usage example:
    
    fp = open('my-file.csv', 'wb')
    writer = UnicodeWriter(fp)
    writer.writerows([
        [u'Bob', 22, 7],
        [u'Sue', 28, 6],
        [u'Ben', 31, 8],
        # \xc3\x80 is LATIN CAPITAL LETTER A WITH MACRON
        ['\xc4\x80dam'.decode('utf8'), 11, 4],
    ])
    fp.close()
    """
    def __init__(self, f, dialect=csv.excel_tab, encoding="utf-16", **kwds):
        # Redirect output to a queue
        self.queue = StringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoding = encoding
    
    def writerow(self, row):
        # Modified from original: now using unicode(s) to deal with e.g. ints
        self.writer.writerow([unicode(s).encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = data.encode(self.encoding)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)
    
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)
            

#for i in range(len(venueExamples)):
#    for j in range(len(venueExamples[i])):
#        if type(venueExamples[i][j])==str or type(venueExamples[i][j])==unicode:
#            venueExamples[i][j]= re.sub(r'(,|;)', ' ', venueExamples[i][j]).encode("utf8")




with open("venueExamples.csv", "wb") as f:
    f.write(codecs.BOM_UTF8)
    writer = csv.writer(f,delimiter=',',quotechar='"')
    writer.writerows(venueExamples)
    