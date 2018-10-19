# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Plugin, Citations

from ._formats import (Bowtie2IndexFileFormat, Bowtie2IndexDirFmt)
from ._types import Bowtie2Index
from ._shogun import minipipe
import q2_shogun
from q2_types.feature_data import FeatureData, Taxonomy, Sequence
from q2_types.feature_table import FeatureTable, Frequency
from qiime2.plugin import Int, Float, Range


citations = Citations.load('citations.bib', package='q2_shogun')

plugin = Plugin(
    name='shogun',
    version=q2_shogun.__version__,
    website='https://github.com/qiime2/q2-shogun',
    package='q2_shogun',
    description=('A QIIME 2 plugin wrapper for the SHOGUN shallow shotgun '
                 'sequencing taxonomy profiler.'),
    short_description='Shallow shotgun sequencing taxonomy profiler.',
    citations=[citations['Langmead2012']]
)


plugin.methods.register_function(
    function=minipipe,
    inputs={'input': FeatureData[Sequence],
            'refseqs': FeatureData[Sequence],
            'reference_taxonomy': FeatureData[Taxonomy],
            'database': Bowtie2Index},
    parameters={'taxacut': Float % Range(0.0, 1.0, inclusive_end=True),
                'threads': Int % Range(1, None),
                'percent_id': Float % Range(0.0, 1.0, inclusive_end=True)},
    outputs=[('taxa_table', FeatureTable[Frequency]),
             ('kegg_table', FeatureTable[Frequency]),
             ('module_table', FeatureTable[Frequency]),
             ('pathway_table', FeatureTable[Frequency])],
    input_descriptions={'input': 'Sequences to classify taxonomically.',
                        'refseqs': 'reference sequences.',
                        'reference_taxonomy': 'reference taxonomy labels.',
                        'database': 'bowtie2 index artifact.'},
    parameter_descriptions={
        'taxacut': 'Minimum fraction of assignments must match top '
                   'hit to be accepted as consensus assignment. Must '
                   'be in range (0.0, 1.0].',
        'threads': 'Number of threads to use.',
        'percent_id': 'Reject match if percent identity to query is '
                      'lower. Must be in range [0.0, 1.0].',
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


plugin.register_semantic_types(Bowtie2Index)
plugin.register_semantic_type_to_format(
    Bowtie2Index, artifact_format=Bowtie2IndexDirFmt)
plugin.register_formats(Bowtie2IndexFileFormat, Bowtie2IndexDirFmt)
