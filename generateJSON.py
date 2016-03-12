
# coding: utf-8

# In[276]:

import pandas as pd
import requests as req
from json import loads, dumps
import time 
import uuid

# turn off column width
#pd.set_option('display.max_colwidth', -1)


# In[137]:

cols = ["country", "state", "city", "fbURL", "gmapsURL", "gmapsJSON"]
campsites = pd.read_csv('campsitesLocationInfo2.csv', sep="|", header=None)
campsites.columns = cols


# In[138]:

#no null values
campsites.info()


# In[139]:

# some duplcaite locations (gmapsJSON) and fb URLS
# NOTE: duplicate city names are okay and expected
campsites.describe()


# In[140]:

print 'here are some duplicates facebook groups:'
dupFB = campsites[campsites['fbURL'].duplicated(False)]
print dupFB[['city', 'fbURL']]
print "these looks intentional"


# In[141]:

print 'here are some duplicates google map responses:'
dupLocations = campsites['gmapsJSON'].duplicated(False)
print campsites[dupLocations]
print "It looks like:"
print "-Kingston upon Hull and Hull are the same place according to google maps"
print "-Women only group didn't have a city"
print "-Hampton Roads is in Virginia"
print "NOTE: Dropping these for now, but could be handled better"
campsites = campsites[~dupLocations]


# In[ ]:




# In[84]:

# MODEL FOR POSTING 
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


# In[288]:

parsedLocations = campsites
# build list of dicts to create
toCreate = []
for index, row in parsedLocations.iterrows():
    createDict = {}
    # parse info out of dataframe
    createDict['city'] = row['city']
    createDict['subdivision'] = row['state']
    createDict['country'] = row['country']
    createDict['url'] = row['fbURL']
    # load gmaps json
    gmapsInfo = loads(row['gmapsJSON'])['results'][0]
    loc = gmapsInfo['geometry']['location']
    createDict['location'] = str(loc['lat']) + ',' + str(loc['lng'])
    createDict['googleId'] = str(gmapsInfo['place_id'])
    # NOTE: mapURL is missing and requires another lookup :/
    
    # add other info
    now = time.strftime('%c')
    createDict['id'] = uuid.uuid4().hex
    createDict['createdByUsername'] = 'BULKCAMPSITEUPLOAD'
    createDict['createdAt'] = now
    createDict['lastUpdatedAt'] = now
    createDict['isApproved'] = False # requires approval
    createDict['isDeleted'] = False 
    # append json
    toCreate.append(createDict)
    


# In[273]:

# write out json to file 
with open('toWrite.json', 'w') as fp:
    for campsite in toCreate:
        data = dumps(campsite)
        fp.write(data + "\n")


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



