#usr/bin/awk -f

# example URL: https://maps.googleapis.com/maps/api/geocode/json?address=Mountain+View,+CA
BEGIN{BASEURL="https://maps.googleapis.com/maps/api/geocode/json?address=" }
{
  original=$0
  gsub(/ /, "+"); # replace spaces with +
  split($0,a,"|"); # split on pipes
  if (a[2] == "none"){
    # handle case where no level2 location
    url=BASEURL a[3]","a[1]
  } else {
    url=BASEURL a[3]","a[2]","a[1]
  }
  print original"|"url
} 
