#usr/bin/awk -f

# variables to keep track of values at indendation depths
BEGIN{level1=""; level2=""; level3="";}
# skip intro lines
NR == 1, NR==3 { next } {
  # new country
  if(/^- /) {
    gsub(/^- /, ""); # remove opening dash and space
    gsub(/[ \t]+$/, ""); # replace trailing whitespace
    level1=$0
  }
  # handle level 2
  if(/^  -/) {
    gsub(/^  - /, ""); #  remove opening dash and spaces
    gsub(/[ \t]+$/, ""); # replace trailing whitespace
    # handle case where level2 is a campsite
    if(!/[ a-zA-Z]+$/) {
      gsub(/\[/, ""); # get rid of opening [
      gsub(/\)/, ""); # get rid of closing )
      gsub(/\]\(/, "|"); # replace middle with seperator that can be parsed
      line=level1"|none|"$0 
      print line
    } else {
      # handle case where level 2 is a location
      level2=$0
    }
  }
  # handle level 3
  if(/^    -/) {
    gsub(/^    - /, "");  #remove opening dash and spaces
    gsub(/[ \t]+$/, ""); # replace trailing whitespace
    gsub(/\[/, ""); # get rid of opening [
    gsub(/\)/, ""); # get rid of closing )
    gsub(/\]\(/, "|"); # replace middle with seperator that can be parsed
    line=level1"|"level2"|"$0 
    print line
    
  }  
}
