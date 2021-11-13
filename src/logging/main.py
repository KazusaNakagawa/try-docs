import json
import uuid

import logging.config


def read_conf_file(conf_file='conf/conf.json'):
    """ 設定ファイル読み込み """
    with open(conf_file, 'r', encoding='utf-8') as f:
        f_ = json.load(f)
        logging.config.dictConfig(f_)


def get_logger(logger_='simpleDefault'):
    """ ロガー生成 """
    return logging.getLogger(logger_)


def get_user_id(user_id):
    return user_id


def main():
    # 設定ファイル読み込み
    # read_conf_file(conf_file='conf/conf.json')
    # read_conf_file(conf_file='conf/syslog.json')
    read_conf_file(conf_file='conf/filehandler.json')

    # logger 読み込み
    logger = get_logger(logger_='simpleDefault')
    logger = get_logger(logger_='')

    user_id = get_user_id(1)

    # 引数はカスタマイズできる
    # logger.debug({
    #     'debug': 'debug message',
    #     'id': user_id,
    # }, extra={'user_id': user_id})

    logger.debug('debug message', extra={'user_id': user_id})
    logger.info('info message', extra={'user_id': user_id})
    logger.warning('warning message', extra={'user_id': user_id})
    logger.error('error message', extra={'user_id': user_id})
    logger.critical('critical message', extra={'user_id': user_id})


if __name__ == '__main__':
    main()
