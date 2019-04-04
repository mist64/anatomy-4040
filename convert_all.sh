#!/bin/bash
for i in `cat order.txt | grep -v ^#`; do
	echo "<!--- ***** $i --->"
	python3 convert.py files/$i
done
