import configparser
import json
import logging
import uuid

import os
from logging import StreamHandler, FileHandler, Formatter
from logging import INFO, DEBUG, NOTSET

import logging.config

_EXEC_FILE_NAME = os.path.basename(__file__)[:-3]


def read_conf_file(conf_file='format/conf.json'):
    """ Loading a format file """
    with open(conf_file, 'r', encoding='utf-8') as f:
        f_ = json.load(f)
        logging.config.dictConfig(f_)


def get_logger(logger_='simpleDefault'):
    """ ロガー生成 """
    return logging.getLogger(logger_)


def get_conf(conf, sec: str, option: str, format1=None, format2=None):
    """ Get the section name and key. """
    conf = conf.get(section=sec, option=option)
    return conf.format(format1, format2)


def set_file_handler(logger):
    if not os.path.isdir('./log'):
        os.makedirs('./log', exist_ok=True)

    read_conf_file(conf_file='format/mulch.json')
    return get_logger(logger)
