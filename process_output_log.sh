#!/bin/sh
echo chance_to_win,accuracy,confidence,loss,ticker > $1.csvt
cat $1 | grep -e "24[01234]\/24[01234] \[==============================\]" -e conf | sed ':a;N;$!ba;s/\nSystem/ System/g' | grep System  |  awk '{ print $11" "$23" "$8" "$18 }' | sort | awk '{ if($1>0.0){result=$1 * $2; printf "%0.8f %0.8f %0.8f %0.8f %s\n",result,$1,$2,$3,$4}}'  >> $1.csvt ; 
cat $1.csvt | tr ' ' ',' > $1.csv
rm $1.csvt
python ./parse_filtered_output_csv.py $1.csv | sort -n
