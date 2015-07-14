#!/usr/bin/env Rscript
suppressPackageStartupMessages(library("MALDIquant"))
suppressPackageStartupMessages(library("MALDIquantForeign"))

args <- commandArgs(trailingOnly = TRUE)

inputFile <- args[1]

s <- importCsv(inputFile)

s <- s[[1]]

p <- detectPeaks(s, method="MAD", halfWindowSize=20, SNR=10)

inputFile1 = strsplit(inputFile, split=".", fixed=TRUE)

outputFile = paste(inputFile1[[1]][1],".","peaklist",sep="")

exportCsv(p, file=outputFile, force=TRUE)