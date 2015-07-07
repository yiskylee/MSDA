#for file in `find /home/xiangyu/Documents/PROTECT/csv/ -name "*.csv" -not -path "/home/xiangyu/Documents/PROTECT/csv/boston/*"`
for file in `find /home/xiangyu/PROTECT/csv/ -name "*.csv"`
do 
  #echo $file
  Rscript findPeaks.R $file
done
