import json
import logging
import os

import logging.config


class LogConf(object):
    """ log Setting Class """

    def __init__(self):
        pass

    def _read_conf_file(self, conf_file: str) -> None:
        """ log 設定ファイルの読み込み

        :param
          conf_file(str): log 設定ファイル名
        :return:
          None
        """
        with open(conf_file, 'r', encoding='utf-8') as f:
            f_ = json.load(f)
            logging.config.dictConfig(f_)

    def get_logger(self, logger: str, conf_file='format/log_format/mulch.json') -> logging.Logger:
        """ log 出力フォーマットを指定して、log 出力する

        :param
          logger: logger 生成
          conf_file: log 設定ファイル
        :return:
          生成した logger (logging.Logger)
        """
        if not os.path.isdir('./log'):
            os.makedirs('./log', exist_ok=True)

        self._read_conf_file(conf_file=conf_file)

        filename, _ = os.path.splitext(os.path.basename(logger))
        logger = logging.getLogger(filename)

        # log 出力使用可能に設定
        logger.disabled = False

        return logger

    def _get_conf(self, conf, sec: str, option: str, format1=None, format2=None):
        """ Get the section name and key. """
        conf = conf.get(section=sec, option=option)
        return conf.format(format1, format2)
