#!/bin/sh


rm output.log 

rm ./all_stocks_5yr.csv
cd stocks
rm * -rf
cd ..
python getSandP.py
./merge.sh

z=0
for i in `seq 0 2`; do 
	for x in `seq 0 2`; do
		b=256
		a=""
		if [ $i -lt 2 ]; then
			a="-a"
		fi
		if [ $i -eq 2 ]; then
			b=32
		fi  
		while ( ! ( python stacked_lstm.py -p=./all_stocks_5yr.csv -t=$i -b=$b $a -r ) ); do 
			b=`expr $b \/ 2`
		done
		z=`expr $z + 1`
	done
done | tee output.log
