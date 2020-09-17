# -*- coding: utf-8 -*-

import logging
import string
import os
from urllib.parse import urljoin

import click
import bioblend.galaxy

from workflow2executable.invocations import InvocationMonitor

log = logging.Logger(__name__)
log.setLevel(logging.INFO)
# create a console handler with INFO loglevel
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
log.addHandler(ch)

FULL_WORKFLOW = None


@click.command("Run MIRACUM - report panel variants workflow")
@click.option("--sample_identifier", type=str)
@click.option("--gemini_db_of_variants", type=click.Path())
@click.option("--uniprot_annotated_cancer_genes", type=click.Path())
@click.option("--cgi_listed_genes", type=click.Path())
@click.option("--civic_genes", type=click.Path())
@click.option('-a', '--api_key', help="API key to use for running workflow")
@click.option('-g', '--galaxy_url', default="https://usegalaxy.org", help="Galaxy URL to use for running workflow", show_default=True)
@click.option('-h', '--history_id', help="History ID that will contain workflow results")
@click.option('-n', '--new_history_name', help="Create a new history with this name. Will not be used if history ID is provided.")
@click.option('--publish/--private', default=False, help="Publish history?")
@click.option('--monitor_invocation/--no_monitor_invocation', default=False, help="Print workflow invocation status updates?")
@click.option('--workflow_id_override', default=None, help="Override workflow to run with this workflow id or uuid")
@click.option('--quiet', default=False, help='Decrease logging output')
def run_miracum___report_panel_variants(sample_identifier, gemini_db_of_variants, uniprot_annotated_cancer_genes, cgi_listed_genes, civic_genes, api_key, galaxy_url, history_id, new_history_name, publish, monitor_invocation, workflow_id_override, quiet):
    """
    Run MIRACUM - report panel variants workflow

    Produce tabular and MAF (cBioportal-compatible) reports of annotated variants.
    """
    if quiet:
        log.setLevel(logging.ERROR)
    gi = bioblend.galaxy.GalaxyInstance(galaxy_url, api_key)
    workflow_id = workflow_id_override or 'dac845d5-e89c-4b4f-84a3-118b9965bacf'
    try:
        gi.workflows.show_workflow(workflow_id)
    except Exception:
        if FULL_WORKFLOW:
            gi.workflows.import_workflow_dict(FULL_WORKFLOW)
            log.info("Imported workflow")
        else:
            raise Exception("Workflow with id '%s' not uploaded or not accessible" % workflow_id)
    if history_id is None:
        if new_history_name is None:
            new_history_name = 'History for MIRACUM - report panel variants execution'
        history = gi.histories.create_history(name=new_history_name)
    else:
        history = gi.histories.show_history(history_id)
    history_id = history['id']
    if publish:
        history = gi.histories.update_history(history_id, published=True, importable=True)
        history_url = urljoin(galaxy_url, history['username_and_slug'])
    else:
        history_url = urljoin(galaxy_url, "histories/view?id=%s" % history_id)
    # This will look a bit awkward,
    # those could become custom click types
    datasets_to_upload = [gemini_db_of_variants, uniprot_annotated_cancer_genes, cgi_listed_genes, civic_genes]
    upload_paths = {}
    for dataset in datasets_to_upload:
        if os.path.exists(dataset):
            log.info("Uploading dataset '%s' to history %s", dataset, history_url)
            r = gi.tools.upload_file(path=dataset, history_id=history_id, to_posix_lines=False)
            upload_paths[dataset] = {'src': 'hda', 'id': r['outputs'][0]['id']}
        elif all(c in string.hexdigits for c in dataset):
            log.info("Importing dataset '%s' to history %s", dataset, history_url)
            try:
                _ = gi.datasets.show_dataset(dataset)
                source = 'hda'
            except bioblend.ConnectionError:
                _ = gi.datasets.show_dataset(dataset, hda_ldda='ldda')
                source = 'library'
            r = gi.histories.copy_dataset(history_id=history_id, dataset_id=dataset, source=source)
            upload_paths[dataset] = {'src': 'hda', 'id': r['id']}
        else:
            raise ValueError(
                "Failed to locate dataset '%s'! No file system match and does "
                "not look like a valid dataset id.",
                dataset
            )

    inputs = {
        'Sample identifier': upload_paths.get(sample_identifier, sample_identifier),
        'GEMINI DB of variants': upload_paths.get(gemini_db_of_variants, gemini_db_of_variants),
        'UniProt-annotated cancer genes': upload_paths.get(uniprot_annotated_cancer_genes, uniprot_annotated_cancer_genes),
        'CGI-listed genes': upload_paths.get(cgi_listed_genes, cgi_listed_genes),
        'CIViC genes': upload_paths.get(civic_genes, civic_genes),
    }
    invocation = run_workflow(gi, workflow_id, history_id, inputs)
    assert invocation['state'] == 'new', "Expected invocation state to be 'new', but invocation is %s" % invocation
    log.info("Workflow '%s' started with invocation id '%s'. Results will appear in history %s", workflow_id, invocation['id'], history_url)
    if monitor_invocation:
        im = InvocationMonitor(gi)
        im.monitor_invocation(invocation['id'])


def run_workflow(gi, workflow_id, history_id, inputs):
    r = gi.workflows.invoke_workflow(
        workflow_id,
        inputs=inputs,
        history_id=history_id,
        inputs_by='name',
    )
    return r


if __name__ == '__main__':
    run_miracum___report_panel_variants()
