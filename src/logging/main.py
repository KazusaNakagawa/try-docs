import logging
import uuid
import logging.config

# logging.config.fileConfig('conf/conf.json')
#
# with open('conf/conf.json', 'r', encoding='utf-8') as f:
#     conf_file = f.read()
#
# logging.config.dictConfig(conf_file)
import uuid

logging.config.dictConfig(
    {
        "version": 1,
        "formatters": {
            "sampleFormatter": {
                "format": "%(asctime)s %(name)-12s %(levelname)-8s %(name)-15s %(message)s"}
        },
        "handlers": {
            "sampleHandlers": {
                "class": "logging.StreamHandler",
                "formatter": "sampleFormatter",
                "level": logging.DEBUG,
            }
        },

        "root": {
            "handlers": ["sampleHandlers"],
            "level": logging.WARNING
        },
        "loggers": {
            "simpleExample": {
                "handlers": ["sampleHandlers"],
                "level": logging.DEBUG,
                "propagate": 0
            },
            "simpleExample2": {
                "handlers": ["sampleHandlers"],
                "level": logging.CRITICAL,
                "propagate": 0
            },
        }
    }
)

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
