# ----------------------------------------------------------------------------
# Copyright (c) 2016-2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import Plugin, Citations

import q2_shogun

citations = Citations.load('citations.bib', package='q2_shogun')
plugin = Plugin(
    name='shogun',
    version=q2_shogun.__version__,
    website='https://github.com/qiime2/q2-shogun',
    package='q2_shogun',
    description=('A QIIME 2 plugin wrapper for the SHOGUN shallow shotgun '
                 'sequencing taxonomy profiler.'),
    short_description='Shallow shotgun sequencing taxonomy profiler.'
)
