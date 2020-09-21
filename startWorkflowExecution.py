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

    def get_datasets(self, limit=500, offset=0):
        params = {
            'limit': limit,
            'offset': offset,
        }
        return self._get(params=params)

    def download_dataset(self, dataset_id, file_path=None, use_default_filename=True, maxwait=12000):
        dataset = self._block_until_dataset_terminal(dataset_id, maxwait=maxwait)
        if not dataset['state'] == 'ok':
            raise DatasetStateException("Dataset state is not 'ok'. Dataset id: %s, current state: %s" % (dataset_id, dataset['state']))

        file_ext = dataset.get('file_ext')
        # Resort to 'data' when Galaxy returns an empty or temporary extension
        if not file_ext or file_ext == 'auto' or file_ext == '_sniff_':
            file_ext = 'data'
        # The preferred download URL is
        # '/api/histories/<history_id>/contents/<dataset_id>/display?to_ext=<dataset_ext>'
        # since the old URL:
        # '/dataset/<dataset_id>/display/to_ext=<dataset_ext>'
        # does not work when using REMOTE_USER with access disabled to
        # everything but /api without auth
        download_url = dataset['download_url'] + '?to_ext=' + file_ext
        url = urljoin(self.gi.base_url, download_url)

        stream_content = file_path is not None
        r = self.gi.make_get_request(url, stream=stream_content)
        r.raise_for_status()

        if file_path is None:
            if 'content-length' in r.headers and len(r.content) != int(r.headers['content-length']):
                log.warning("Transferred content size does not match content-length header (%s != %s)", len(r.content), r.headers['content-length'])
            return r.content
        else:
            if use_default_filename:
                # Build a useable filename
                filename = dataset['name'] + '.' + file_ext
                # Now try to get a better filename from the response headers
                # We expect tokens 'filename' '=' to be followed by the quoted filename
                if 'content-disposition' in r.headers:
                    tokens = list(shlex.shlex(r.headers['content-disposition'], posix=True))
                    try:
                        header_filepath = tokens[tokens.index('filename') + 2]
                        filename = os.path.basename(header_filepath)
                    except (ValueError, IndexError):
                        pass
                file_local_path = os.path.join(file_path, filename)
            else:
                file_local_path = file_path

            with open(file_local_path, 'wb') as fp:
                for chunk in r.iter_content(chunk_size=bioblend.CHUNK_SIZE):
                    if chunk:
                        fp.write(chunk)

            # Return location file was saved to
            return file_local_path

class HistoryClient(Client):
    
    def __init__(self, galaxy_instance):
        self.module = 'histories'
        super().__init__(galaxy_instance)
    
    def show_matching_datasets(self, history_id, name_filter=None):
        """
        Get dataset details for matching datasets within a history.

        :type history_id: str
        :param history_id: Encoded history ID

        :type name_filter: str
        :param name_filter: Only datasets whose name matches the
                            ``name_filter`` regular expression will be
                            returned; use plain strings for exact matches and
                            None to match all datasets in the history.
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
    

print(hl)

find_id = hl
get_id = json.loads(find_id)
hh = gi.histories.show_history(history_id = get_id["id"], contents=True, deleted=None, visible=True, details=True, types=None)
sd = gi.histories.show_matching_datasets(history_id = get_id["id"], name_filter=None)
print(hh)
print(sd)
    
    os.system(
        "python3 run_workflow_panel_variant_annotation.py --variants_input --dbsnp_annotations abafdf086c375ee5 --cancerhotspots_data__bed_ c344e7e8c8cc61aa --civic_data__bed_ 3031e83883b39f24 --cgi_biomarkers__bed_ 8aab8fda5bfd5997 --api_key 64b1a4440d46af31d546df70cc5db50d --galaxy_url  http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=86cf1d3beeec9f1c --new_history_name UKER" + str(
            l))

    os.system(
        "python3 run_workflow_panel_report_variant.py  --sample_identifier UKER" + str(
            l) + "--gemini_db_of_variants --uniprot_annotated_cancer_genes 07acaf50ebe1f533 --cgi_listed_genes 8aab8fda5bfd5997  --civic_genes d513c0e53ab96eac --api_key 64b1a4440d46af31d546df70cc5db50d --galaxy_url http://srv-ap-omics1.srv.uk-erlangen.de/ --workflow_id_override=8c959c9304a2bc4b")

    download_dataset(history_id='UKER' + str(l), dataset_id='', file_path='/home/neugebax/UKER' + str(l) + 'main', user_default_filename=False)
    download_dataset(history_id='UKER' + str(l), dataset_id='', file_path='/home/neugebax/UKER' + str(l) + 'annotation', user_default_filename=False)
    download_dataset(history_id='UKER' + str(l), dataset_id='', file_path='/home/neugebax/UKER' + str(l) + 'report', user_default_filename=False)

    delete_history(self, 'UKER' + str(l), purge=True)

    l += 1
