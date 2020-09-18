#! /usr/bin/env python
# -*- coding: utf8 -*-

import os
import glob

data = glob.glob('/Volumes/Base/PycharmProjects/MTB/*_R1_merged.fastq.gz')

l = 0

for filename in data:
    os.system()
        "python3 run_workflow_panel_main.py --forward_reads UKER" + str(l) + "_R1_merged.fastq.gz --reverse_reads UKER" + str(l) + "_R1_merged.fastq.gz --dbsnp_records abafdf086c375ee5 --api_key 64b1a4440d46af31d546df70cc5db50d --galaxy_url http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=a0c15f4d91084599 --new_history_name UKER" + str(l) ")
    l += 1