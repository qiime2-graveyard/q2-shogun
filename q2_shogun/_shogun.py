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

import biom
import qiime2


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
             reference_taxonomy: pd.Series, database : bowtieindex,
             taxacut: float=0.8,
             threads: int=1, percent_id: float=0.98) -> pd.DataFrame:
    with tempfile.NamedTemporaryFile() as tmp:
        # generate the expected database dir structure
        copyfile(str(refseqs), os.path.join(tmp, 'seqs.fasta'))
        copyfile(str(reference_taxonomy), os.path.join(tmp, 'taxa.tsv'))
        metadata_fp = os.path.join(tmp, 'metadata.yaml')
        with open(metadata_fp, 'w') as metadata_f:
            metadata_f.write('general:\n'
                             '  taxonomy: taxa.tsv\n'
                             '  fasta: seqs.fasta\n'
                             'bowtie2: {0}'.format(bowtieindex))

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


plugin.methods.register_function(
    function=minipipe,
    inputs={'input': FeatureData[Sequence],
            'refseqs': FeatureData[Sequence],
            'reference_taxonomy': FeatureData[Taxonomy],
            'database': BowtieIndex[Genome]},
    parameters={'taxacut': Float % Range(0.0, 1.0, inclusive_end=True),
                'threads': Int % Range(1, None),
                'percent_id': Float % Range(0.0, 1.0, inclusive_end=True)},
    outputs=[('taxa_table', FeatureTable[Frequency]),
             ('kegg_table', FeatureTable[Frequency]),
             ('module_table', FeatureTable[Frequency]),
             ('pathway_table', FeatureTable[Frequency])],
    input_descriptions={'query': 'Sequences to classify taxonomically.',
                        'reference_reads': 'reference sequences.',
                        'reference_taxonomy': 'reference taxonomy labels.',
                        'database': 'bowtie2 index artifact.'},
    parameter_descriptions={
        'taxacut': 'Minimum fraction of assignments must match top '
                   'hit to be accepted as consensus assignment. Must '
                   'be in range (0.0, 1.0].',
        'threads': 'Number of threads to use.',
        'percent_id': 'Reject match if percent identity to query is '
                      'lower. Must be in range [0.0, 1.0].')
    },
    output_descriptions={
        'taxa_table': 'Frequency table of taxonomic composition.',
        'kegg_table': 'Frequency table of KEGG ortholog composition.',
        'module_table': 'Frequency table of KEGG module composition.',
        'pathway_table': 'Frequency table of KEGG pathway composition.'},
    name='SHOGUN bowtie2 taxonomy and functional profiler',
    description=('Profile query sequences functionally and taxonomically '
                 'using via alignment with bowtie2, followed by LCA taxonomy '
                 'assignment.')
)
