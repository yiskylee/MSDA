suppressPackageStartupMessages(library("MALDIquant"))
suppressPackageStartupMessages(library("MALDIquantForeign"))
args <- commandArgs(trailingOnly = TRUE)
inputFile = args[1]
s <- importCsv(inputFile)
#s <- importCsv("/home/xiangyu/Documents/PROTECT/csv/boston/100_MS_59.csv")
s = s[[1]]
p <- detectPeaks(s, method="MAD", halfWindowSize=20, SNR=10)
#xlim <- range(mass(s))
#plot(s, main="peaks", sub="", xlim=xlim)
#points(p)
## label top 20 peaks
#top20 <- intensity(p) %in% sort(intensity(p), decreasing=TRUE)[1:20]
#labelPeaks(p, index=top20, underline=TRUE)
inputFile1 = strsplit(inputFile, split=".", fixed=TRUE)
outputFile = paste(inputFile1[[1]][1],".","peaklist",sep="")
outputFile = gsub("csv","peaklist",outputFile)
exportCsv(p, file=outputFile, force=TRUE)
