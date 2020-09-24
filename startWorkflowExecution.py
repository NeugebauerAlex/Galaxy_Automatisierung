#! /usr/bin/env python
# -*- coding: utf8 -*-

import os
import glob
import logging
import re
import sys
import time
import json

var = True
import bioblend
from bioblend import galaxy
from bioblend.galaxy.client import Client

l = 26

gi = galaxy.GalaxyInstance(url='http://srv-ap-omics1.srv.uk-erlangen.de/', key='64b1a4440d46af31d546df70cc5db50d')
hl = gi.histories.get_histories()


class DatasetClient(Client):

    def __init__(self, galaxy_instance):
        self.module = 'datasets'
        super(DatasetClient, self).__init__(galaxy_instance)

    def get_datasets(self, limit=500, offset=0):
        params = {
            'limit': limit,
            'offset': offset,
        }
        return self._get(params=params)

    def download_dataset(self, history_id, dataset_id, file_path,
                         use_default_filename=True):
        """
        .. deprecated:: 0.8.0
           Use :meth:`~bioblend.galaxy.datasets.DatasetClient.download_dataset`
           instead.
        """
        meta = self.show_dataset(history_id, dataset_id)
        if use_default_filename:
            file_local_path = os.path.join(file_path, meta['name'])
        else:
            file_local_path = file_path
        return self.gi.datasets.download_dataset(dataset_id,
                                                 file_path=file_local_path,
                                                 use_default_filename=False)

class HistoryClient(Client):
    
    def __init__(self, galaxy_instance):
        self.module = 'histories'
        super().__init__(galaxy_instance)
    
    def get_histories(self, history_id=None, name=None, deleted=False):
        """
        """
        if history_id is not None and name is not None:
            raise ValueError('Provide only one argument between name or history_id, but not both')
        histories = self._get(deleted=deleted)
        if history_id is not None:
            history = next((_ for _ in histories if _['id'] == history_id), None)
            histories = [history] if history is not None else []
        elif name is not None:
            histories = [_ for _ in histories if _['name'] == name]
        return histories

    def show_matching_datasets(self, history_id, name_filter=None):
        """
        """
        if isinstance(name_filter, basestring):
            name_filter = re.compile(name_filter + '$')
        return [self.show_dataset(history_id, h['id'])
                for h in self.show_history(history_id, contents=True)
                if name_filter is None or name_filter.match(h['name'])]

    def delete_history(self, history_id, purge=True):
        payload = {}
        if purge is True:
            payload['purge'] = purge
        return self._delte(payload=payload, id=history_id)
    
    def show_history(self, history_id, contents=True, deleted=None, visible=True, details=True, types=None):
        params = {}
        if contents:
            if details:
                params['details'] = details
            if deleted is not None:
                params['deleted'] = deleted
            if visible is not None:
                params['visible'] = visible
            if types is not None:
                params['types'] = types
        return self._get(id=history_id, contents=contents, params=params)

data = glob.glob('/home/neugebax/galaxy-test/*_R1_merged.fastq.gz')

for filename in data:
    os.system(
        "python3 run_workflow_panel_main.py --forward_reads UKER" + str(
            l) + "_R1_merged.fastq.gz --reverse_reads UKER" + str(
            l) + "_R1_merged.fastq.gz --dbsnp_records abafdf086c375ee5 --api_key 64b1a4440d46af31d546df70cc5db50d --galaxy_url http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=a0c15f4d91084599 --new_history_name UKER" + str(
            l))
    

    hh = gi.histories.get_histories(history_id=None, name="UKER" +str(l), deleted=False)
    li = [item.get('id') for item in hh]




  #  sd = gi.histories.show_matching_datasets(history_id = get_id["id"], name_filter=None)
 
    
 #   os.system(
 #       "python3 run_workflow_panel_variant_annotation.py --variants_input --dbsnp_annotations abafdf086c375ee5 --cancerhotspots_data__bed_ c344e7e8c8cc61aa --civic_data__bed_ 3031e83883b39f24 --cgi_biomarkers__bed_ 8aab8fda5bfd5997 --api_key 64b1a4440d46af31d546df70cc5db50d --galaxy_url  http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=86cf1d3beeec9f1c --new_history_name UKER" + str(
 #           l))

 #   os.system(
  #      "python3 run_workflow_panel_report_variant.py  --sample_identifier UKER" + str(
  #          l) + "--gemini_db_of_variants --uniprot_annotated_cancer_genes 07acaf50ebe1f533 --cgi_listed_genes 8aab8fda5bfd5997  --civic_genes d513c0e53ab96eac --api_key 64b1a4440d46af31d546df70cc5db50d --galaxy_url http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=8c959c9304a2bc4b")

    gi.histories.download_dataset(history_id=li[0], dataset_id='', file_path='/home/neugebax/UKER_main', use_default_filename=True)
   # gi.histories.download_dataset(history_id= li, dataset_id='', file_path='/home/neugebax/UKER' + str(l) + 'annotation', use_default_filename=True)
   # gi.histories.download_dataset(history_id= li, dataset_id='', file_path='/home/neugebax/UKER' + str(l) + 'report', use_default_filename=True)

   # gi.histories.delete_history(self, li, purge=True)

    l += 1
