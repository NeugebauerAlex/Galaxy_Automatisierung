#! /usr/bin/env python
# -*- coding: utf8 -*-

import os
import glob

var = True
from bioblend import galaxy

gi = galaxy.GalaxyInstance(url='http://srv-ap-omics1.srv.uk-erlangen.de/', key='64b1a4440d46af31d546df70cc5db50d')
hist = gi.histories.get_histories()

def delete_history(self, history_id, purge=True):
    payload = {}
    if purge is True:
        payload['purge'] = purge
    return self._delte(payload=payload, id=history_id)


def download_dataset(self, history_id, dataset_id, file_path, user_default_filename=True):
    meta = self.show_dataset(history_id, dataset_id)
    if user_default_filename:
        file_local_path = os.path.join(file_path, meta['name'])
    else:
        file_local_path = file_path
    return self.gi.datasets.download_dataset(dataset_id, file_path=file_local_path, user_default_filename=False)


data = glob.glob('/home/neugebax/galaxy-test/*_R1_merged.fastq.gz')

l = 26

for filename in data:
    os.system(
        "python3 run_workflow_panel_main.py --forward_reads UKER" + str(
            l) + "_R1_merged.fastq.gz --reverse_reads UKER" + str(
            l) + "_R1_merged.fastq.gz --dbsnp_records abafdf086c375ee5 --api_key 64b1a4440d46af31d546df70cc5db50d --galaxy_url http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=a0c15f4d91084599 --new_history_name UKER" + str(
            l))
    
    
    os.system(
        "python3 run_workflow_panel_variant_annotation.py --variants_input --dbsnp_annotations abafdf086c375ee5 --cancerhotspots_data__bed_ c344e7e8c8cc61aa --civic_data__bed_ 3031e83883b39f24 --cgi_biomarkers__bed_ 8aab8fda5bfd5997 --api_key 64b1a4440d46af31d546df70cc5db50d --galaxy_url  http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=86cf1d3beeec9f1c --new_history_name UKER" + str(
            l))

    os.system(
        "python3 run_workflow_panel_report_variant.py  --sample_identifier UKER" + str(
            l) + "--gemini_db_of_variants --uniprot_annotated_cancer_genes 07acaf50ebe1f533 --cgi_listed_genes 8aab8fda5bfd5997  --civic_genes d513c0e53ab96eac --api_key 64b1a4440d46af31d546df70cc5db50d --galaxy_url http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=8c959c9304a2bc4b")

    download_dataset(self, "UKER" + str(l), dataset_id='', file_path='/Desktop/Ergebnisse_workflow/UKER' + str(l) + "main", user_default_filename=False)
    download_dataset(self, "UKER" + str(l), dataset_id='', file_path='/Desktop/Ergebnisse_workflow/UKER' + str(l) + "annotation", user_default_filename=False)
    download_dataset(self, "UKER" + str(l), dataset_id='', file_path='/Desktop/Ergebnisse_workflow/UKER' + str(l) + "report", user_default_filename=False)

    delete_history(self, "UKER" + str(l), purge=True)

    l += 1
