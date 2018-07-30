#!/bin/bash

echo "date,open,high,low,close,volume,Name" > all_stocks_5yr.csv
cd stocks
files=$(ls *.csv)
for file in $files
do
	tail -n +2 $file >> ../all_stocks_5yr.csv
done