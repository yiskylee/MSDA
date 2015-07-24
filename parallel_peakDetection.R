library("readMzXmlData")
library("MALDIquant")
library("MALDIquantForeign")

filename = "DENAMIC_Luba_24042015_nepos_16.mzXML"

xml <- readMzXmlData::readMzXmlFile(filename, 
                                    removeMetaData = TRUE)
## the xml file is a list file, each list is a retention time data set
## for each list, it contain spectrum and metaData lists.
## Inside spectrum list, there are mass and intensity lists.
## For instance,
## $ :List of 2
## ..$ spectrum:List of 2
## .. ..$ mass     : num [1:1874] 57 57 57 57 57 ...
## .. ..$ intensity: num [1:1874] 1105 2833 6086 16030 20041 ...
## ..$ metaData:List of 1
print(system.time(
ms <- lapply(xml, function(x){
    createMassSpectrum(x$spectrum$mass, 
                       x$spectrum$intensity, 
                       metaData = list(name=x$metaData$file))})
))


ms_seq = vector(mode="list", length = length(xml))

print(system.time(
for (i in 1:length(xml))
{
    ms_seq[i]<- createMassSpectrum(xml[[i]]$spectrum$mass, 
                       xml[[i]]$spectrum$intensity, 
                       metaData = list(name=xml[[i]]$metaData$file))
}
))

## run single-core baseline correction
print(system.time(
    p <- detectPeaks(ms, method="MAD", halfWindowSize=20, SNR=10)
))

## run multi-core baseline correction
if(.Platform$OS.type == "unix") 
{
    print(system.time(
        p1 <- detectPeaks(ms, 
                          method="MAD", halfWindowSize=20, SNR=10,
                          mc.cores=4)
    ))
    print(all.equal(p, p1))
}


## export peaklist
for(i in 1:length(p))
{
    inputFile = strsplit(filename, split=".", fixed=TRUE)
    outputFile = paste(inputFile[[1]][1],"_", i , ".", "peaklist",sep="")
    # print(outputFile)
    exportCsv(p[[i]], file=outputFile, force=TRUE)
}


