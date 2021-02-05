# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import os
import subprocess
import tempfile
import shutil

import yaml
import biom
import pandas as pd
from qiime2.util import duplicate
from q2_types.feature_data import DNAFASTAFormat

from q2_types.bowtie2 import Bowtie2IndexDirFmt


def _run_command(cmd, verbose=True):
    if verbose:
        print("Running external command line application. This may print "
              "messages to stdout and/or stderr.")
        print("The command being run is below. This command cannot "
              "be manually re-run as it will depend on temporary files that "
              "no longer exist.")
        print("\nCommand:", end=' ')
        print(" ".join(cmd), end='\n\n')
    subprocess.run(cmd, check=True)


def setup_database_dir(tmpdir, database, refseqs, reftaxa):
    BOWTIE_PATH = 'bowtie2'
    duplicate(str(refseqs), os.path.join(tmpdir, 'refseqs.fna'))
    reftaxa.to_csv(os.path.join(tmpdir, 'taxa.tsv'), sep='\t')
    shutil.copytree(str(database), os.path.join(tmpdir, BOWTIE_PATH),
                    copy_function=duplicate)
    params = {
        'general': {
            'taxonomy': 'taxa.tsv',
            'fasta': 'refseqs.fna'
        },
        'bowtie2': os.path.join(BOWTIE_PATH, database.get_basename())
    }
    with open(os.path.join(tmpdir, 'metadata.yaml'), 'w') as fh:
        yaml.dump(params, fh, default_flow_style=False)


def load_table(tab_fp):
    '''Convert classic OTU table to biom feature table'''
    with open(tab_fp, 'r') as tab:
        return biom.table.Table.from_tsv(tab, None, None, None)


def nobunaga(query: DNAFASTAFormat, reference_reads: DNAFASTAFormat,
             reference_taxonomy: pd.Series, database: Bowtie2IndexDirFmt,
             taxacut: float = 0.8,
             threads: int = 1, percent_id: float = 0.98) -> biom.Table:
    with tempfile.TemporaryDirectory() as tmpdir:
        setup_database_dir(tmpdir,
                           database, reference_reads, reference_taxonomy)

        # run aligner
        cmd = ['shogun', 'align', '-i', str(query), '-d', tmpdir,
               '-o', tmpdir, '-a', 'bowtie2', '-x', str(taxacut),
               '-t', str(threads), '-p', str(percent_id)]
        _run_command(cmd)

        # assign taxonomy
        taxatable = os.path.join(tmpdir, 'taxatable.tsv')
        cmd = ['shogun', 'assign_taxonomy', '-i',
               os.path.join(tmpdir, 'alignment.bowtie2.sam'), '-d', tmpdir,
               '-o', taxatable, '-a', 'bowtie2']
        _run_command(cmd)

        # output taxatable as feature table
        return load_table(taxatable)


def minipipe(query: DNAFASTAFormat, reference_reads: DNAFASTAFormat,
             reference_taxonomy: pd.Series, database: Bowtie2IndexDirFmt,
             taxacut: float = 0.8,
             threads: int = 1, percent_id: float = 0.98) -> (
                     biom.Table, biom.Table, biom.Table, biom.Table):
    with tempfile.TemporaryDirectory() as tmpdir:
        setup_database_dir(tmpdir,
                           database, reference_reads, reference_taxonomy)

        # run pipeline
        cmd = ['shogun', 'pipeline', '-i', str(query), '-d', tmpdir,
               '-o', tmpdir, '-a', 'bowtie2', '-x', str(taxacut),
               '-t', str(threads), '-p', str(percent_id)]
        _run_command(cmd)

        # output selected results as feature tables
        tables = ['taxatable.strain.txt',
                  'taxatable.strain.kegg.txt',
                  'taxatable.strain.kegg.modules.txt',
                  'taxatable.strain.kegg.pathways.txt']
        return tuple(load_table(os.path.join(tmpdir, t)) for t in tables)
