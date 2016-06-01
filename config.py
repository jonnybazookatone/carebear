# encoding: utf-8
"""
Configuration file. Please prefix application specific config values with
the application name.
"""

import os

LOG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../')
)
LOG_PATH = '{home}/logs/'.format(home=LOG_PATH)

if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)

# For running tests on TravisCI
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:password@localhost:5433/carebear'

CAREBEAR_LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(levelname)s\t%(process)d '
                      '[%(asctime)s]:\t%(message)s',
            'datefmt': '%m/%d/%Y %H:%M:%S',
        }
    },
    'handlers': {
        'console': {
            'formatter': 'default',
            'level': 'DEBUG',
            'class': 'logging.StreamHandler'
        }
    },
    'loggers': {
        '': {
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


