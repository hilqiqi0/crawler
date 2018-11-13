#!/bin/sh
export PATH=$PATH:/usr/local/bin
ls_date=`date +%Y-%m-%d_%H:%M:%S`
mkdir log/${ls_date} -p
cd log/${ls_date}
echo $1
for((i=1;i<=$1;i++));
do
time scrapy crawl blbl >> $i.txt 2>&1 &
done

