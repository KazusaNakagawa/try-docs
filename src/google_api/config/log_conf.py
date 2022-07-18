import json
import logging
import os

import logging.config


def _read_conf_file(conf_file: str) -> None:
    """ log 設定ファイルの読み込み

    :param
      conf_file(str): log 設定ファイル名
    :return:
      None
    """
    with open(conf_file, 'r', encoding='utf-8') as f:
        f_ = json.load(f)
        logging.config.dictConfig(f_)


def _get_logger(logger_: str) -> logging.Logger:
    """ log 出力名設定

    :param
      logger_(str): log 出力名
    :return:
      生成した logger (logging.Logger)
    """
    return logging.getLogger(logger_)


def _get_conf(conf, sec: str, option: str, format1=None, format2=None):
    """ Get the section name and key. """
    conf = conf.get(section=sec, option=option)
    return conf.format(format1, format2)


def set_file_handler(logger, conf_file='format/log_format/mulch.json') -> logging.Logger:
    """ log 出力フォーマットを指定して、log 出力する

    :param
      logger: logger 生成
      conf_file: log 設定ファイル
    :return:
      生成した logger (logging.Logger)
    """
    if not os.path.isdir('./log'):
        os.makedirs('./log', exist_ok=True)

    _read_conf_file(conf_file=conf_file)
    return _get_logger(logger)
