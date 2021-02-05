# ----------------------------------------------------------------------------
# Copyright (c) 2018-2021, QIIME 2 development team.
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
        self.taxatable = _load('taxatable.qza')

    def test_nobunaga(self):
        taxa = shogun.actions.nobunaga(
            query=self.query, reference_reads=self.refseqs,
            reference_taxonomy=self.taxonomy, database=self.database)
        observed_taxa_table = taxa.taxa_table.view(biom.Table).\
            sort(axis='observation').sort(axis='sample')

        expected_taxa_table = self.taxatable.view(biom.Table).\
            sort(axis='observation').sort(axis='sample')

        observed_feature_ids = set(observed_taxa_table.ids(axis='observation'))
        expected_feature_ids = set(expected_taxa_table.ids(axis='observation'))
        self.assertEqual(observed_feature_ids, expected_feature_ids)

        observed_sample_ids = set(observed_taxa_table.ids(axis='sample'))
        expected_sample_ids = set(expected_taxa_table.ids(axis='sample'))
        self.assertEqual(observed_sample_ids, expected_sample_ids)

        report = observed_taxa_table.descriptive_equality(expected_taxa_table)
        self.assertIn('Tables appear equal', report, report)


if __name__ == '__main__':
    unittest.main()
