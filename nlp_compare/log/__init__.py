#####################################################################################
# Copyright (c) 2017,2025 Wowool, All Rights Reserved.
# NOTICE:  All information contained herein is, and remains the property of Wowool.
#####################################################################################
import logging
import logging.config

# from logging import FileHandler, StreamHandler
from pathlib import Path

LOGGIN_CONFIG_FILE = Path("logging.conf")
LOGGIN_CONFIG_DATA = """[loggers]
keys=root,nlp_engine,stanza

[handlers]
keys=consoleHandler,fileHandler

[formatters]
keys=default

[logger_root]
level=INFO
handlers=consoleHandler

[logger_stanza]
level=ERROR
handlers=consoleHandler
qualname=stanza
propagate=0

[logger_nlp_engine]
level=INFO
handlers=consoleHandler
qualname=nlp_engine
propagate=0

[handler_consoleHandler]
class=StreamHandler
level=DEBUG
formatter=default
args=(sys.stdout,)

[handler_fileHandler]
class=FileHandler
level=DEBUG
formatter=default
args=('app.log', 'a')

[formatter_default]
_format=%(levelname)s:%(module)s: %(message)s
__format=%(asctime)s - %(name)s - %(levelname)s - %(message)s
format=%(asctime)s - %(levelname)s - %(message)s

"""


def safe_initialize_logging_config():
    if not LOGGIN_CONFIG_FILE.exists():
        LOGGIN_CONFIG_FILE.write_text(LOGGIN_CONFIG_DATA)
    logging.config.fileConfig(LOGGIN_CONFIG_FILE)


def initialize_logging_level():
    safe_initialize_logging_config()
