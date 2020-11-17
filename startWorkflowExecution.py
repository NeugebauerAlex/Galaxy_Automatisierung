#! /usr/bin/env python
# -*- coding: utf8 -*-

import os
import glob
import logging
import re
import sys
import time
import json
import logging
import shlex
import time
import os.path 

var = True
import bioblend
from bioblend import galaxy
from bioblend.galaxy.client import Client

l = 40 
m = 60
z = 1200
t = 9400

gi = galaxy.GalaxyInstance(url='http://srv-ap-omics1.srv.uk-erlangen.de/', key='a7066326d337da43021b076aaf79124a')
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

data = glob.glob('/care/storage-normal/Galaxy_files/*_R1_merged.fastq.gz')

for filename in data:
    
    if l > 0:
        path = '/care/storage-normal/Galaxy_files/UKER{}'.format(l)
        if not os.path.exists(path):
            os.mkdir(path)

    os.system(
        "python3 run_workflow_panel_main.py --sample_name UKER --forward_reads UKER" + str(
           l) + "_R1_merged.fastq.gz --reverse_reads UKER" + str(
            l) + "_R2_merged.fastq.gz --dbsnp_records abafdf086c375ee5 --api_key a7066326d337da43021b076aaf79124a --galaxy_url http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=f1b9846ab84237e7 --new_history_name UKER" + str(
           l))
    

    hh = gi.histories.get_histories(history_id=None, name="UKER" +str(l), deleted=False)
    li = [item.get('id') for item in hh]
    li_element = li[0]
    li_element_string = str(li_element)

    # Warte bis Durchgang fertig ist
    time.sleep(t)

    no_data = gi.histories.show_history(li_element, contents=False)
    find_id = no_data['state_ids']['ok']
    find_id_safe = find_id[25]
  
    #Warte kurz bis zweiter Workflow losgeht
    time.sleep(m)

    #Starte zweiten Workflow
    input = (find_id_safe)

    os.system(
      "python3 run_workflow_panel_variant_annotation.py --variants_input %s --dbsnp_annotations abafdf086c375ee5 --cancerhotspots_data__bed_ 74a1c2b9ba2a073a --civic_data__bed_ d513c0e53ab96eac --cgi_biomarkers__bed_ 3b06f51e28371f42 --api_key a7066326d337da43021b076aaf79124a --galaxy_url  http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=84ffe6fca6c4fbda --new_history_name UKER_ZWEI"%input)
    
    # History ID des zweiten Workflows herauskriegen
    zw = gi.histories.get_histories(history_id=None, name="UKER_ZWEI", deleted=False)
    zi = [item.get('id') for item in zw]
    zi_element = zi[0]
    zi_element_string = str(zi_element)  

    # Warte bis Durchgang vollzogen ist 
    time.sleep(z)

    # Dataset ID finden und herunterladen
    data_set_zwei = gi.histories.show_history(zi_element, contents=False)
    find_id_zwei = data_set_zwei['state_ids']['ok']
    find_id_safe_zwei = find_id_zwei[13] 

    #Warte kurz bis dritter Workflow losgeht
    time.sleep(m)

    # Starte dritten Workflow
    input = (find_id_safe_zwei)
    
    os.system(
        "python3 run_workflow_panel_report_variant.py  --sample_identifier UKER --gemini_db_of_variants %s --uniprot_annotated_cancer_genes 07acaf50ebe1f533 --cgi_listed_genes 8aab8fda5bfd5997 --civic_genes c9213a53ccefcc61 --api_key a7066326d337da43021b076aaf79124a --galaxy_url http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=6f91353f3eb0fa4a --new_history_name UKER_DREI"%input)

    # Warte bis Durchgang vollzogen ist 
    time.sleep(m)

    # History ID des dritten Workflows herauskriegen
    ll = gi.histories.get_histories(history_id=None, name="UKER_DREI", deleted=False)
    bi = [item.get('id') for item in ll]
    bi_element = bi[0]
    bi_element_string = str(bi_element)

    # Dataset ID finden und herunterladen
    data_set_drei = gi.histories.show_history(bi_element, contents=False)
    find_id_drei = data_set_drei['state_ids']['ok']
    maf_report = find_id_drei[4]
    annotation_report = find_id_drei[5]
    gene_report = find_id_drei[10]

    # Lade das Dataset herunter
    gi.histories.download_dataset(history_id=bi_element, dataset_id=maf_report, file_path='/care/storage-normal/Galaxy_files/UKER{}'.format(l), use_default_filename=True)
    gi.histories.download_dataset(history_id=bi_element, dataset_id=annotation_report, file_path='/care/storage-normal/Galaxy_files/UKER{}'.format(l), use_default_filename=True)
    gi.histories.download_dataset(history_id=bi_element, dataset_id=gene_report, file_path='/care/storage-normal/Galaxy_files/UKER{}'.format(l), use_default_filename=True)

    #Warte kurz bis löschen von Histories losgeht
    time.sleep(m)

    # History löschen funktioniert
    gi.histories.delete_history(history_id=li_element, purge=True)
    gi.histories.delete_history(history_id=zi_element, purge=True)
    gi.histories.delete_history(history_id=bi_element, purge=True)

    l += 1