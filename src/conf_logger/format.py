import configparser
import logging


def set_conf(conf_file='msg_format.ini'):
    conf = configparser.ConfigParser()
    conf.read(conf_file)
    return conf


def get_conf(conf, sec: str, option: str, format1=None, format2=None):
    conf = conf.get(section=sec, option=option)
    return conf.format(format1, format2)


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
