import unittest
from nation_flags.settings import config

class TestSettings(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_config_is_not_none(self):
        self.assertIsNotNone(config)