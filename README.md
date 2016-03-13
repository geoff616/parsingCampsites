##Summary:

This repo contains a set of scripts that migrate data contained in the FreeCodeCamp Wiki page: List-of-Free-Code-Camp-city-based-Campsites.md to the database developed for the `feature/campsite-db` pull request. 

##How it works:
The main script `generateCampsites.sh` performs the following steps:

1. Download the Markdown page with the latest list of campsites from the DCC Wiki with `cURL`
2. Run `parseCampsites.awk` to create a csv from the Markdown page
3. Run `parseCampsiteURLs.awk` to create the URLs needed to request the location info from Google Maps
4. `cURLs` all of those URL's and does a second pass to retry any faliures from the first pass
5. Run `generateJSON.py` to validate the data and saves the JSON needed to POST to the FCC API
6. Use `native2ascii` to unencode the unicode characters
7. `cURL` the FCC API with each campsite's JSON to save the records to the DB
