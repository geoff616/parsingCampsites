# This script is meant to migrate the campsites listed on the wiki page
# to the campsite-db feature. 

#filenames to use
wikiFile="campsitesWiki.MD" 
parsedWiki="campsitesParsed.csv"
urlsToQuery="campsitesGoogleMapsURLS.csv"
googleMapResponses="campsitesLocationInfo.csv"
secondPassAtGoogleMapQueries="campsitesLocationInfo2.csv"

# download latest markdown file
curl https://raw.githubusercontent.com/FreeCodeCamp/wiki/master/List-of-Free-Code-Camp-city-based-Campsites.md > $wikiFile

# parse markdown file 
awk -f parseCampsites $wikiFile > $parsedWiki

#generate urls from file

awk -f parseCampsiteURLs $parsedWiki > $urlsToQuery

# query urls and save responses
# NOTE: There is no error handling for this, but can count the number of status "OK"s
# failed responses have line endings that match "|$" regex
while read line ; do
  url=`echo $line | awk -F"|" '{print $5}'`
  resp=$(curl -N --globoff $url | tr -d "\n")
  echo $line"|"$resp >> $googleMapResponses
done < $urlsToQuery

echo "campsites that failed google maps query:"
count=$(cat $googleMapResponses | grep \|$ | wc -l)
echo $count
# retry failed queries - where last character in the line is a pipe
# NOTE: only had a handfull ~5 out of 1000+ fail, and this was simple fix
while read line ; do
  # last character is pipe, retry
  if [ "${line: -1}" == "|" ]
  then
    url=`echo $line | awk -F"|" '{print $5}'`
    resp=$(curl -N --globoff $url | tr -d "\n")
    echo $line$resp >> $secondPassAtGoogleMapQueries
  else 
    echo $line >> $secondPassAtGoogleMapQueries
  fi
done < $googleMapResponses
echo "campsites that failed second pass at google maps query:"
count=$(cat $secondPassAtGoogleMapQueries | grep \|$ | wc -l)
echo $count
echo "generating post bodies in python"
python generateJSON.py

echo "making a bunch of http requests to create campsites"
while read body ; do
  curl -X POST --header "Content-Type: application/json" --header "Accept: application/json" -d "$body" "http://127.0.0.1:3000/api/campsites"
done < toWrite.json


echo "all done - hope that worked!"

