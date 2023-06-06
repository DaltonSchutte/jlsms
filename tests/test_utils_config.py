import os
import yaml

import pytest

import sys
sys.path.insert(0, '..')

from src import ROOT_DIR
from src.utils import config

TEST_CONFIG = 'demo_config.yaml'

class TestValidateConfigExtension:
    def test_valid(self):
        config.validate_config_path(TEST_CONFIG)

    def test_valid_yml(self):
        config.validate_config_path("demo_config.yml")

    def test_invalid(self):
        with pytest.raises(ValueError):
            config.validate_config_path("bad_config_ext.txt")

class TestLoadGdeltConfig:
    @pytest.fixture(autouse=True)
    def test_load(self):
        self.config = config.load_gdelt_config(TEST_CONFIG)
        assert isinstance(self.config, dict)

    def test_version(self):
        assert self.config['version'] == 2

    def test_table(self):
        assert self.config['table'] == 'events'

    def test_output(self):
        assert self.config['output'] == 'csv'

class TestLoadEntireConfig:
    @pytest.fixture(autouse=True)
    def test_load(self):
        self.config = config.load_entire_config(TEST_CONFIG)
        assert isinstance(self.config, dict)

    def test_missing_keys(self):
        missing = []
        for key in self.config.keys():
            if key not in config.CONFIG_COMPONENTS:
                missing.append(key)
        if len(missing) > 0:
            msg = (
                f"Missing keys: {', '.join(missing)}. "
                f"Expected: {', '.join(config.CONFIG_COMPONENTS)}"
            )
            raise KeyError(msg)

class TestLoadConfig:
    def test_load_error(self):
        with pytest.raises(ValueError):
            config.load_config(type='xyz', config=TEST_CONFIG)

    def test_load_entire_config(self):
        test_config = config.load_config(type="full", config=TEST_CONFIG)
        assert isinstance(test_config, dict)
