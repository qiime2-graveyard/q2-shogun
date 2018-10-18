# ----------------------------------------------------------------------------
# Copyright (c) 2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from qiime2.plugin import model


class Bowtie2IndexFileFormat(model.BinaryFileFormat):
    def _validate_(self, level):
        # It's not clear if there is any way to tell if a Bowtie2 index is
        # correct or not.
        pass


class Bowtie2IndexDirFmt(model.DirectoryFormat):
    idx1 = model.File('.+\.1\.bt2', format=Bowtie2IndexFileFormat)
    idx2 = model.File('.+\.2\.bt2', format=Bowtie2IndexFileFormat)
    ref3 = model.File('.+\.3\.bt2', format=Bowtie2IndexFileFormat)
    ref4 = model.File('.+\.4\.bt2', format=Bowtie2IndexFileFormat)
    rev1 = model.File('.+\.rev\.1\.bt2', format=Bowtie2IndexFileFormat)
    rev2 = model.File('.+\.rev\.2\.bt2', format=Bowtie2IndexFileFormat)
