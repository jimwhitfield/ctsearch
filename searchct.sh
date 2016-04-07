#!/bin/bash

if [ ! "$1" -o ! "$2" ]
then
  echo "First arg is search term, second is destination parent folder"
  exit 1
fi
echo Searching for $1

sanitized_search_term=$1
sanitized_search_term="${sanitized_search_term//[^-A-Za-z0-9]/_}"

mkdir $2
time_str=$(date "+%Y-%m-%d__%H:%M:%S")
echo writing download to $time_str.zip in $2.  Will extract to $2/$sanitized_search_term
curl "https://clinicaltrials.gov/ct2/results/download?down_stds=all&down_typ=study&down_flds=all&down_fmt=xml&recr=Open&term=$1" > $2/$time_str.zip
(cd $2; mkdir $sanitized_search_term; unzip -d $sanitized_search_term $time_str.zip)