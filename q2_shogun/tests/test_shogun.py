# ----------------------------------------------------------------------------
# Copyright (c) 2018-2019, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest
from warnings import filterwarnings

import qiime2
import biom
from qiime2.plugins import shogun
from qiime2.plugin.testing import TestPluginBase

filterwarnings("ignore", category=UserWarning)
filterwarnings("ignore", category=RuntimeWarning)


class TestShogun(TestPluginBase):
    package = 'q2_shogun.tests'

    def setUp(self):
        super().setUp()

        def _load(fp):
            return qiime2.Artifact.load(self.get_data_path(fp))

        self.database = _load('bt2-database.qza')
        self.query = _load('query.qza')
        self.refseqs = _load('refseqs.qza')
        self.taxonomy = _load('taxonomy.qza')
        self.taxatable = _load('taxatable.qza').view(biom.Table)

    # def test_minipipe(self):
    #    taxa, kegg, modules, pathways = shogun.actions.minipipe(
    #        query=self.query, reference_reads=self.refseqs,
    #        reference_taxonomy=self.taxonomy, database=self.database)

    def test_nobunaga(self):
        taxa = shogun.actions.nobunaga(
            query=self.query, reference_reads=self.refseqs,
            reference_taxonomy=self.taxonomy, database=self.database)
        taxa.taxa_table.view(biom.Table).descriptive_equality(self.taxatable)


if __name__ == '__main__':
    unittest.main()
