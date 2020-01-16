# ----------------------------------------------------------------------------
# Copyright (c) 2018-2020, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from ._version import get_versions
from ._formats import (Bowtie2IndexFileFormat, Bowtie2IndexDirFmt)
from ._types import Bowtie2Index


__version__ = get_versions()['version']
del get_versions

__all__ = ['Bowtie2IndexFileFormat', 'Bowtie2IndexDirFmt', 'Bowtie2Index']
