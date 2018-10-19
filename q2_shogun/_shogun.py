# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import subprocess
import tempfile
from shutil import copyfile
import os

import pandas as pd
import biom
import qiime2
from ._types import Bowtie2Index
from q2_types.feature_data import DNAFASTAFormat


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


def minipipe(input: DNAFASTAFormat, refseqs: DNAFASTAFormat,
             reference_taxonomy: pd.Series, database: Bowtie2Index,
             taxacut: float=0.8, threads: int=1, percent_id: float=0.98
             ) -> (biom.Table, biom.Table, biom.Table, biom.Table):
    with tempfile.NamedTemporaryFile() as tmp:
        # generate the expected database dir structure
        copyfile(str(refseqs), os.path.join(tmp, 'seqs.fasta'))
        copyfile(str(reference_taxonomy), os.path.join(tmp, 'taxa.tsv'))
        metadata_fp = os.path.join(tmp, 'metadata.yaml')
        with open(metadata_fp, 'w') as metadata_f:
            metadata_f.write('general:\n'
                             '  taxonomy: taxa.tsv\n'
                             '  fasta: seqs.fasta\n'
                             'bowtie2: {0}'.format(database))

        # run pipeline
        cmd = ['shogun', 'pipeline', '-i', input, '-d', tmp, '-o', tmp,
               '-a', 'bowtie2', '-x', taxacut, '-t', threads, '-p', percent_id]
        _run_command(cmd)

        # output selected results as feature tables
        tables = ['taxatable.strain.txt',
                  'taxatable.strain.kegg.txt',
                  'taxatable.strain.kegg.modules.txt',
                  'taxatable.strain.kegg.pathways.txt']
        return (import_table(os.path.join(tmp, t)) for t in tables)


def import_table(tab_fp):
    '''Convert classic OTU table to biom feature table'''
    table = biom.table.Table.from_tsv(tab_fp, None, None, None)
    return qiime2.Artifact.import_data('FeatureTable[Frequency]', table)
