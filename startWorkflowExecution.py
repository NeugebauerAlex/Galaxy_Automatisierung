#! /usr/bin/env python
# -*- coding: utf8 -*-

import os
import glob

data = glob.glob('/Volumes/Base/PycharmProjects/MTB/*_R1_merged.fastq.gz')

l = 0

for filename in data:
    os.system(
        "python3 run_workflow_panel_main.py --normal_forward_reads UKER" + str(l) + "_R1_merged.fastq.gz --regions Galaxy13-[capture_targets_chr5_12_17.bed].bed --normal_reverse_reads UKER" + str(l) + "_R2_merged.fastq.gz --tumor_forward_reads UKER26_R1_merged.fastq.gz  --tumor_reverse_reads UKER26_R2_merged.fastq.gz --galaxy_url https://usegalaxy.eu --api_key 64b1a4440d46af31d546df70cc5db50d --workflow_id_override=132016f833b57406")
    l += 1