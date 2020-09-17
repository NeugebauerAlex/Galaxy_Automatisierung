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


@click.command("Run Miracum - panel main workflow")
@click.option("--sample_name", type=str)
@click.option("--forward_reads", type=click.Path())
@click.option("--reverse_reads", type=click.Path())
@click.option("--dbsnp_records", type=click.Path())
@click.option('-a', '--api_key', help="API key to use for running workflow")
@click.option('-g', '--galaxy_url', default="https://usegalaxy.org", help="Galaxy URL to use for running workflow", show_default=True)
@click.option('-h', '--history_id', help="History ID that will contain workflow results")
@click.option('-n', '--new_history_name', help="Create a new history with this name. Will not be used if history ID is provided.")
@click.option('--publish/--private', default=False, help="Publish history?")
@click.option('--monitor_invocation/--no_monitor_invocation', default=False, help="Print workflow invocation status updates?")
@click.option('--workflow_id_override', default=None, help="Override workflow to run with this workflow id or uuid")
@click.option('--quiet', default=False, help='Decrease logging output')
def run_miracum___panel_main(sample_name, forward_reads, reverse_reads, dbsnp_records, api_key, galaxy_url, history_id, new_history_name, publish, monitor_invocation, workflow_id_override, quiet):
    """
    Run Miracum - panel main workflow

    Generate a list of variants (VCF) from paired sequenced gene panel reads.
    """
    if quiet:
        log.setLevel(logging.ERROR)
    gi = bioblend.galaxy.GalaxyInstance(galaxy_url, api_key)
    workflow_id = workflow_id_override or '201fd660-11ef-446f-9824-2f98ad930d04'
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
            new_history_name = 'History for Miracum - panel main execution'
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
    datasets_to_upload = [forward_reads, reverse_reads, dbsnp_records]
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
        'sample name': upload_paths.get(sample_name, sample_name),
        'forward reads': upload_paths.get(forward_reads, forward_reads),
        'reverse reads': upload_paths.get(reverse_reads, reverse_reads),
        'dbSNP records': upload_paths.get(dbsnp_records, dbsnp_records),
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
    run_miracum___panel_main()
