library("readMzXmlData")
library("MALDIquant")
library("MALDIquantForeign")
library(parallel)


xml <- readMzXmlData::readMzXmlFile("DENAMIC_Luba_24042015_nepos_16.mzXML", 
                                    removeMetaData = TRUE)

## form the MassSpectrum object
ms <- lapply(xml, function(x){
    createMassSpectrum(x$spectrum$mass, 
                       x$spectrum$intensity, 
                       metaData = list(name=x$metaData$file))})

work.single <- function(ms) {
    detectPeaks(ms, method="MAD", halfWindowSize=20, SNR=10) 
}

# mclapply(ms, work_mc, mc.silent = FALSE, mc.cores=4)
print(system.time(
p <- mclapply(ms, work.single, mc.cores = getOption("mc.cores", 6L))
))

