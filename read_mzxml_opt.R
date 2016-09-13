# Usage:
#   Save this script in your mzXML file folder.
#   Run Rscript read_mzxml_opt.R.
#   All the mass and intensity will be exported in csv file.
#
# Author: Leiming Yu
#         ylm@ece.neu.edu


library("MALDIquantForeign")
library("MALDIquant")
library(data.table) 
# library("mzR")
# library("parallel")




args = commandArgs(trailingOnly=TRUE)
if (length(args) != 2) {
  stop("Usage: Rscript read_mzxml_opt.R input_dir output_dir", call.=TRUE)
}
input_dir <- args[1]
output_dir <- args[2]
allfile <- list.files(path=input_dir, pattern="*.mzXML")

for (fid in 1:length(allfile))
{
  ## read read file, and export the csv
  
  #-----------------------------------------------------------------------------------------------------#
  ## read mzXML, save to mass spectrum class
  #-----------------------------------------------------------------------------------------------------#
  input_file_name = paste(input_dir, allfile[fid], sep='')
  ms <- importMzXml(input_file_name, removeMetaData = TRUE, verbose = FALSE)
  
  #-----------------------------------------------------------------------------------------------------#
  ## accumulate the intensity for each scan
  #-----------------------------------------------------------------------------------------------------#
  num_scans <- length(ms)
  
  data <- list()
  
  for (i in 1:num_scans)
  {
    id_ = as.character(i)
    mass_ = mass(ms[[i]])
    intensity_ = intensity(ms[[i]])
    data[[i]] = data.frame(Scan_id = id_, Mass = mass_, Intensity = intensity_) 
  }
  
  data <- rbindlist(data) 
  print(allfile[fid])
  
  # output csv
  file_title <- strsplit(allfile[fid], split=".", fixed=TRUE)
  output_file_title <- paste(file_title[[1]][1], ".csv", sep='')
  output_file_name <- paste(output_dir, output_file_title, sep='')
  write.csv(data, file=output_file_name, row.names=FALSE)
}
