import configparser
import json
import logging
import uuid

import os
from logging import StreamHandler, FileHandler, Formatter
from logging import INFO, DEBUG, NOTSET

import logging.config


def read_conf_file(conf_file='conf/conf.json'):
    """ Loading a format file """
    with open(conf_file, 'r', encoding='utf-8') as f:
        f_ = json.load(f)
        logging.config.dictConfig(f_)


def get_logger(logger_='simpleDefault'):
    """ ロガー生成 """
    return logging.getLogger(logger_)


def get_user_id(user_id):
    return user_id


def set_conf(conf_file='conf/msg_format.ini'):
    """ Read the format file you set. """
    conf = configparser.ConfigParser()
    conf.read(conf_file)
    return conf


def get_conf(conf, sec: str, option: str, format1=None, format2=None):
    """ Get the section name and key. """
    conf = conf.get(section=sec, option=option)
    return conf.format(format1, format2)


def test1():
    set_conf_ = set_conf()
    msg = get_conf(conf=set_conf_, sec='message', option='EAP0001', format1=[1, 2, 3], format2=[1, 2, 3])
    logging.error(msg)

    msg = get_conf(conf=set_conf_, sec='message', option='EAP0002', format1=[1, 2, 3])
    logging.warning(msg)

    msg = get_conf(conf=set_conf_, sec='message', option='EAP0003', format1=[1, "ID0001"])
    logging.debug(msg)
    logging.info(msg)
    logging.warning(msg)
    logging.error(msg)
    logging.critical(msg)


def test2():
    """ Run """
    # read_conf_file(conf_file='conf/conf.json')
    # read_conf_file(conf_file='conf/syslog.json')
    # read_conf_file(conf_file='conf/filehandler.json')
    # read_conf_file(conf_file='conf/file_stream_handler.json')
    read_conf_file(conf_file='conf/mulch.json')

    # 指定 logger 読み込み
    logger = get_logger(logger_='root')

    user_id = get_user_id(uuid.uuid4())

    # message definition file set/get
    set_conf_ = set_conf()
    msg1 = get_conf(conf=set_conf_, sec='message', option='EAP0001', format1=[1, 2, 3], format2=[1, 2, 3])
    msg2 = get_conf(conf=set_conf_, sec='message', option='EAP0002', format1=[1, 2, 3])
    msg3 = get_conf(conf=set_conf_, sec='message', option='EAP0003', format1=[user_id, "ID0001"])

    logger.debug(msg1)
    logger.info(msg1)
    logger.warning(msg2)
    logger.error(msg3)
    logger.critical(f'critical message {msg1}')


def mulch_handler_set():
    # 保存先の有無チェック
    _LOG_LEVEL = DEBUG

    if not os.path.isdir('./Log'):
        os.makedirs('./Log', exist_ok=True)

    # ファイルハンドラの設定
    file_handler = FileHandler(
        # f"./Log/log{datetime.now():%Y%m%d%H%M%S}.log"
        f"./Log/log"
    )
    file_handler.setLevel(_LOG_LEVEL)
    file_handler.setFormatter(
        Formatter("%(asctime)s %(name)-15s %(levelname)-13s %(message)s　%(process)d")
    )
    # ストリームハンドラの設定
    stream_handler = StreamHandler()
    stream_handler.setLevel(_LOG_LEVEL)
    stream_handler.setFormatter(Formatter("%(asctime)s %(name)-15s %(levelname)-13s %(message)s　%(process)d"))
    # ルートロガーの設定
    logging.basicConfig(level=_LOG_LEVEL, handlers=[stream_handler, file_handler])


def mulch_handler():
    # message definition file set/get
    mulch_handler_set()

    set_conf_ = set_conf()
    msg1 = get_conf(conf=set_conf_, sec='message', option='EAP0001', format1=[1, 2, 3], format2=[1, 2, 3])
    msg2 = get_conf(conf=set_conf_, sec='message', option='EAP0002', format1=[1, 2, 3])
    # user_id = get_user_id(uuid.uuid4())
    # msg3 = get_conf(conf=set_conf_, sec='message', option='EAP0003', format1=[user_id, "ID0001"])

    # 出力テスト
    logging.debug(msg1)
    logging.info(msg2)
    logging.warning(msg1)
    logging.error(msg2)
    logging.critical(msg1)


def sample_python_doc():
    logger = logging.getLogger(os.path.basename(__file__)[:-3])
    logger.setLevel(logging.DEBUG)

    # create file handler which logs even debug messages
    fh = logging.FileHandler('./log/spam.log')
    fh.setLevel(logging.DEBUG)

    # create console handler with a higher log level
    ch = logging.StreamHandler()
    ch.setLevel(logging.ERROR)

    # create formatter and add it to the handlers
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    # add the handlers to logger
    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


if __name__ == '__main__':
    pass
    # mulch_handler()
    test2()

