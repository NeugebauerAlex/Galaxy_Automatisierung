#! /usr/bin/env python
# -*- coding: utf8 -*-

import os
import glob

data = glob.glob('/Volumes/Base/PycharmProjects/MTB/*_R1_merged.fastq.gz')

l = 0

for filename in data:
    os.system(
        "python3 run_workflow_panel_main.py --forward_reads UKER" + str(l) + "_R1_merged.fastq.gz --reverse_reads UKER" + str(l) + "_R1_merged.fastq.gz --dbsnp_records abafdf086c375ee5 --api_key 64b1a4440d46af31d546df70cc5db50d --galaxy_url http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=a0c15f4d91084599 --new_history_name UKER" + str(l))

    os.system(
        "python3 run_workflow_panel_variant_annotation.py --variants_input --dbsnp_annotations abafdf086c375ee5 --cancerhotspots_data__bed_ c344e7e8c8cc61aa --civic_data__bed_ 3031e83883b39f24 --cgi_biomarkers__bed_ 8aab8fda5bfd5997 --api_key 64b1a4440d46af31d546df70cc5db50d --galaxy_url  http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=86cf1d3beeec9f1c --new_history_name UKER" + str(l))

    os.system(
        "python3 run_workflow_panel_report_variant.py  --sample_identifier  --gemini_db_of_variants --uniprot_annotated_cancer_genes  --cgi_listed_genes  --civic_genes--api_key 64b1a4440d46af31d546df70cc5db50d --galaxy_url http://srv-ap-omics1.srv.uk-erlangen.de/ --new_history_name" + str(l) + "--workflow_id_override=8c959c9304a2bc4b")

    l += 1