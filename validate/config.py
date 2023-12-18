# Module to load .cfg files

import os
import configparser
import json

def validate_config(dir):
    # Check if the config file exists
    if not os.path.exists(dir):
        return False, "Config file does not exist"
    
    # Check if the config file is a file
    if not os.path.isfile(dir):
        return False, "Config file is not a file"
    
    # Check if the config file is a .cfg file
    if not dir.endswith(".cfg"):
        return False, "Config file is not a .cfg file"
    
    # Check if the config file is a valid .cfg file
    config = configparser.ConfigParser()
    try:
        config.read(dir)
    except:
        return False, "Config file is not a valid .cfg file"
    
    # Check if the config file has log_dir. Not under a section
    if not config.has_option("log_dir"):
        return False, "Config file does not have log_dir"
    
    # Check if the log_dir is a valid directory
    if not os.path.exists(config["log_dir"]):
        return False, "log_dir does not exist"
    
    # Check if the log_dir is a directory
    if not os.path.isdir(config["log_dir"]):
        return False, "log_dir is not a directory"