"""
Utilities to read config files
"""

import os
from typing import (Optional)

import yaml

import sys
sys.path.insert(0, '..')
from src import ROOT_DIR


###########
# GLOBALS #
###########

CONFIG_COMPONENTS = [
    "full",
    "gdelt",
]


#############
# FUNCTIONS #
#############

def validate_config_path(path: str):
    _, extension = os.path.splitext(path)
    if extension not in ['.yaml','.yml']:
        msg = (
            f"Got config with extension {extension} "
            "but expected .yaml or .yml"
        )
        raise ValueError(msg)


def load_config(
    type: str="full",
    config: Optional[str]=None,
):
    """
    General function to load a config file

    Can load a config file using a specific function based on the "type"
    parameter or the full config file

    Parameters
    ----------
    type
        What part of the config file to load
    config
        name of the specific config file

    Raises
    ------
    ValueError:
        raised when an invalid value for "type" is received
    """
    if type == 'gdelt':
        return load_gdelt_config(config)
    if type == "full":
        return load_entire_config(config)
    else:
        msg = (
            f"Unexpected config type {type} "
            f"Expected one of: {', '.join(CONFIG_COMPONENTS)}"
        )
        raise ValueError(msg)


def load_entire_config(config: str):
    """
    Loads the entire config file

    Parameters
    ----------
    config
        name of the specific config file
    """
    validate_config_path(config)
    path = os.path.join(ROOT_DIR, 'configs', config)
    file = open(path, 'r')
    return yaml.safe_load(file)


def load_gdelt_config(config: str):
    """
    Loads only the gdelt arguments of the config file

    Parameters
    ----------
    config
        name of the specific config file
    """
    config = load_entire_config(config)
    return config['gdelt']
