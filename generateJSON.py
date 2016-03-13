
# coding: utf-8

# In[12]:

import pandas as pd
import requests as req
from json import loads, dumps
import time 
import uuid

# uncomment to turn off column width
#pd.set_option('display.max_colwidth', -1)


# In[13]:

# load data into dataframe
campsites = pd.read_csv('data/campsitesLocationInfo2.csv', sep="|", header=None)
cols = ["country", "state", "city", "fbURL", "gmapsURL", "gmapsJSON"]
campsites.columns = cols


# In[14]:

print "check for null values:"
print campsites.info()


# In[15]:

print" check for duplicates"
print "NOTE: duplicate city/state/country names are okay and expected"
print "but would expect fbURL, gmapsURL and gmapsJSON to be unique"
print campsites.describe()


# In[16]:

print 'here are some duplicates facebook groups:'
dupFB = campsites[campsites['fbURL'].duplicated(False)]
print dupFB[['city', 'fbURL']]
print "these looks intentional"


# In[17]:

print 'here are some duplicates google map responses:'
dupLocations = campsites['gmapsJSON'].duplicated(False)
print campsites[dupLocations]
print "It looks like:"
print "-Kingston upon Hull and Hull are the same place according to google maps"
print "-Women only group didn't have a city"
print "-Hampton Roads is in Virginia"
print "NOTE: Dropping these for now, but could be handled better"
droppedLocations = campsites[~dupLocations]


# In[18]:

# MODEL FOR POSTING TO API
## {
##   "id": "string",
##   "url": "string",
##   "createdByUsername": "string",
##   "createdAt": "2016-03-12",
##   "lastUpdatedAt": "2016-03-12",
##   "isApproved": false,
##   "isDeleted": false,
##   "city": "string",
##   "subdivision": "string",
##   "country": "string",
##   "location": "string",
##   "mapURL": "string",
##   "googleId": "string"
## }


# build list of dicts to create
toCreate = []
#loop over cleaned df to build 
for index, row in droppedLocations.iterrows():
    createDict = {}
    # copy info from dataframe
    createDict['city'] = row['city']
    createDict['subdivision'] = row['state']
    createDict['country'] = row['country']
    createDict['url'] = row['fbURL']

    # parse Google maps JSON
    gmapsInfo = loads(row['gmapsJSON'])['results'][0]
    loc = gmapsInfo['geometry']['location']
    createDict['location'] = str(loc['lat']) + ',' + str(loc['lng'])
    createDict['googleId'] = str(gmapsInfo['place_id'])
    # NOTE: mapURL is missing from this API resonse and requires another lookup :/
    
    # add other info
    # unique ID for campsite
    createDict['id'] = uuid.uuid4().hex
    # username to check against in bash script
    createDict['createdByUsername'] = 'BULKCAMPSITEUPLOAD'
    # current time
    now = time.strftime('%c')
    createDict['createdAt'] = now
    createDict['lastUpdatedAt'] = now
    # this automatically approves the campsites, could be set to false 
    # if you want to manually approve 1000+ campsites!
    createDict['isApproved'] = True 
    createDict['isDeleted'] = False 
    # append json to list
    toCreate.append(createDict)
    


# In[19]:

# write out json to file 
with open('data/toWrite.json', 'w') as fp:
    for campsite in toCreate:
        data = dumps(campsite)
        fp.write(data + "\n")

