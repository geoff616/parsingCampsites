# This script is meant to migrate the campsites listed on the wiki page
# to the campsite-db feature. 

#filenames to use
wikiFile="campsitesWiki.MD" 
parsedWiki="campsitesParsed.csv"
urlsToQuery="campsitesGoogleMapsURLS"

# download latest markdown file
curl https://raw.githubusercontent.com/FreeCodeCamp/wiki/master/List-of-Free-Code-Camp-city-based-Campsites.md > $wikiFile

# parse markdown file 
awk -f parseCampsites $wikiFile > $parsedWiki

#generate urls from file

awk -f parseCampsiteURLs $parsedWiki > $urlsToQuery