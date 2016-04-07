#!/usr/bin/python
# Make a series of queries to clinicaltrials.gov, fetching and extracting the results 
#   in a subfolder, optionally named or by default, named with a time stamp
# For demo purposes, we are searching for ones that are recruiting. see recr=Open
# If anyone uses this for real purposes, perhaps you want to add location, say by adding &state1=NA%3AUS%3ACA for Calif

import sys
import os
from datetime import datetime, date, time
import mechanize
import urllib
import zipfile
from bs4 import BeautifulSoup

if (len(sys.argv) <= 1):
    print "ctsearch \"<search string>\"  <parent_dir>"
    sys.exit()
elif (len(sys.argv) == 2):
    search_txt = sys.argv[1]
    now = datetime.today()
    parent_dir = now.strftime("%Y-%m-%d__%H:%M:%S")
    print "ctsearch searching with:",search_txt
    print "***Writing to timestamp directory (",parent_dir,").  To change this, use optional next parameter <parent_dir>"
    os.mkdir(parent_dir)
else:
    search_txt = sys.argv[1]
    parent_dir = sys.argv[2]
    print "ctsearch searching with :",search_txt
    print "Writing to :",parent_dir

# sanitize the name we use for a folder by changing any non-alphanumeric to an underscore
sanitized = "".join([x if x.isalnum() else "_" for x in search_txt])
output_dir = parent_dir + "/" + sanitized
print "About to make output path:",output_dir,"\n** if there is an error following this, perhaps the directory already existed!!"

rtnVal = os.mkdir(output_dir)
print "Successfully created ",output_dir

# Start the search with a minimal page to get going.
# This will fetch "the first n records for web page display, and with a visible form for requesting the whole set."
# (n = 10)
# this maybe wasted effort, at best it's cache warming.  if NIH gave db access, then this would be unneeded
url="https://clinicaltrials.gov/ct2/results?recr=Open&show_down=Y&pg=1&term="+urllib.quote_plus(search_txt)
br = mechanize.Browser()
br.set_handle_robots(False) # ignore robots
br.open(url)

#find the download form the hard way
for form in br.forms():
    if form.attrs['action'] == '/ct2/results/download':
        br.form = form
        break

# mechanize tries to respect hidden fields, but lets me override.
form.set_all_readonly(False)
br["term"]=search_txt
br["recr"]="Open"
br["show_down"]="Y"
br["down_stds"]=["all"]
br["down_typ"]=["study"]
br["down_flds"]=["all"]
br["down_fmt"]=["xml"]
res = br.submit()
content = res.read()

f = open(parent_dir+"/download.zip","w")
f.write(content)
f.close()

f = open(parent_dir+"/download.zip","r")
z = zipfile.ZipFile(f)
z.extractall(output_dir)
        