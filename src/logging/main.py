import logging
import json
import uuid
import logging.config

with open('conf/conf.json', 'r', encoding='utf-8') as f:
    f_ = json.load(f)
    logging.config.dictConfig(f_)

if __name__ == '__main__':
    id_ = uuid.uuid4()

    # logger = logging.getLogger(__name__)
    logger = logging.getLogger('simpleExample')

    logger.debug(
        {'debug': 'debug message',
         'id': id_,
         }
    )
    logger.info('info')
    logger.warning('warning')
    logger.error('error')
    logger.critical('critical')
