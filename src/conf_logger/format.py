import configparser
import json
import logging
import uuid

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


def test_():
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


def main():
    """ Run """
    read_conf_file(conf_file='conf/conf.json')
    # read_conf_file(conf_file='conf/syslog.json')
    # read_conf_file(conf_file='conf/filehandler.json')

    # 指定 logger 読み込み
    logger = get_logger(logger_='simpleDefault')

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


if __name__ == '__main__':
    main()
