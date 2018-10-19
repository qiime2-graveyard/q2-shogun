# ----------------------------------------------------------------------------
# Copyright (c) 2018, QIIME 2 development team.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

import unittest
from warnings import filterwarnings
import pkg_resources

import qiime2
from qiime2.plugins import shogun
from qiime2.plugin.testing import TestPluginBase

filterwarnings("ignore", category=UserWarning)
filterwarnings("ignore", category=RuntimeWarning)


class TestShogun(TestPluginBase):
    package = 'q2_shogun.tests'

    def get_data_path(self, filename):
        return pkg_resources.resource_filename(self.package,
                                               'data/%s' % filename)

    def setUp(self):
        super().setUp()

        def _load(fp):
            return qiime2.Artifact.load(self.get_data_path(fp))

        self.database = _load('bt2-database.qza')
        self.query = _load('query.qza')
        self.refseqs = _load('refseqs.qza')
        self.taxonomy = _load('taxonomy.qza')

    def test_minipipe(self):
        taxa, kegg, modules, pathways = shogun.actions.minipipe(
            query=self.query, reference_reads=self.refseqs,
            reference_taxonomy=self.taxonomy, database=self.database)


if __name__ == '__main__':
    unittest.main()
