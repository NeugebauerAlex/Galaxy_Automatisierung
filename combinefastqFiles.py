#! /usr/bin/env python
# -*- coding: utf8 -*-

import glob
import gzip
import os
import errno
import shutil
from os.path import abspath

k = 41

data = os.listdir('D:\FASTQ_Generation_2020-07-07_05_56_42Z-14283833/')
chunks = [data[x:x+5] for x in range(0, len(data), 5)]

for filename in chunks:
    read_files_R1_V1 = glob.glob('D:\FASTQ_Generation_2020-07-07_05_56_42Z-14283833' + str(k) + '*L001*/*R1*.fastq.gz')
    read_files_R1_V2 = glob.glob('D:\FASTQ_Generation_2020-07-07_05_56_42Z-14283833' + str(k) + '*L002*/*R1*.fastq.gz')
    read_files_R1_V3 = glob.glob('D:\FASTQ_Generation_2020-07-07_05_56_42Z-14283833' + str(k) + '*L003*/*R1*.fastq.gz')
    read_files_R1_V4 = glob.glob('D:\FASTQ_Generation_2020-07-07_05_56_42Z-14283833' + str(k) + '*L004*/*R1*.fastq.gz')
    read_files_R1_FINAl = read_files_R1_V1 + read_files_R1_V2 + read_files_R1_V3 + read_files_R1_V4

    read_files_R2_V1 = glob.glob('D:\FASTQ_Generation_2020-07-07_05_56_42Z-14283833' + str(k) + '*L001/*R2*.fastq.gz')
    read_files_R2_V2 = glob.glob('D:\FASTQ_Generation_2020-07-07_05_56_42Z-14283833' + str(k) + '*L002*/*R2*.fastq.gz')
    read_files_R2_V3 = glob.glob('D:\FASTQ_Generation_2020-07-07_05_56_42Z-14283833' + str(k) + '*L003*/*R2*.fastq.gz')
    read_files_R2_V4 = glob.glob('D:\FASTQ_Generation_2020-07-07_05_56_42Z-14283833' + str(k) + '*L004*/*R2*.fastq.gz')
    read_files_R2_FINAl = read_files_R2_V1 + read_files_R2_V2 + read_files_R2_V3 + read_files_R2_V4
    k += 1

    i = 0
    filename1 = abspath('D:\/MTB/UKER{}_R1_merged.fastq.gz').format(i)
    filename2 = abspath('D:\/MTB/UKER{}_R2_merged.fastq.gz').format(i)

    while os.path.exists(filename1):
        i += 1
        filename1 = abspath('D:\/MTB/UKER{}_R1_merged.fastq.gz').format(i)
        filename2 = abspath('D:\/MTB/UKER{}_R2_merged.fastq.gz').format(i)

    with open(filename1, 'wb') as wfp:
        for fn in read_files_R1_FINAl:
            with open(fn, 'rb') as rfp:
                shutil.copyfileobj(rfp, wfp)

    with open(filename2, 'wb') as wfp:
        for fn in read_files_R2_FINAl:
            with open(fn, 'rb') as rfp:
                shutil.copyfileobj(rfp, wfp)
