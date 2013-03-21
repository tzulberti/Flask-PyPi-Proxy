# -*- coding: utf-8 -*-

''' The main Flask application which take care of reading the configuration.
'''

import os
import json
import logging
from flask import Flask

app = Flask(__name__)


def read_configuration(app, pypi_url='http://pypi.python.org',
                        private_eggs=[]):
    ''' Reads the configuration by using the system file or the configuration
    file.

    :param :class:`Flask` app: the app to where set the configuration values

    :param str pypi_url: the base Pypi url from where get the packages.

    :param str private_eggs: the list of the name of the proyects for which
                             the **pypi_url** won't be used.
    '''
    filepath = os.environ.get('FLASK_PYPI_PROXY_CONFIG')
    if filepath:
        # then the configuration file is used
        if not os.path.exists(filepath):
            raise Exception('There should be a configuration file but '
                            'the path is invalid')

        with open(filepath) as config_file:
            configuration = json.load(config_file)
            if not 'BASE_FOLDER_PATH' in configuration:
                raise Exception('The configuration should have the value '
                                'for BASE_FOLDER_PATH')

            if not 'LOGGING_PATH' in configuration:
                raise Exception('The configuration must have the value for '
                                'LOGGING_PATH')

            app.config['PRIVATE_EGGS'] = configuration.get('PRIVATE_EGGS',
                                                           private_eggs)
            app.config['BASE_FOLDER_PATH'] = configuration['BASE_FOLDER_PATH']
            app.config['SHOULD_USE_EXISTING'] = configuration.get(
                                                        'SHOULD_USE_EXISTING',
                                                        False)
            app.config['PYPI_URL'] = configuration.get('PYPI_URL', pypi_url)
            app.config['LOGGING_PATH'] = configuration.get('LOGGING_PATH')
            app.config['LOGGING_LEVEL'] = configuration.get('LOGGING_LEVEL',
                                                            'DEBUG')

    else:
        base_path = os.environ.get('PYPI_PROXY_BASE_FOLDER_PATH')
        logging_path = os.environ.get('PYPI_PROXY_LOGGING_PATH')
        if not base_path:
            raise Exception('The PYPI_PROXY_BASE_FOLDER_PATH or '
                            'FLASK_PYPI_PROXY_CONFIG environment keys '
                            'are missing')

        if not logging_path:
            raise Exception('The PYPI_PROXY_LOGGING_PATH or '
                            'FLASK_PYPI_PROXY_CONFIG environment keys '
                            'are missing')

        app.config['BASE_FOLDER_PATH'] = base_path
        app.config['LOGGING_PATH'] = logging_path
        app.config['LOGGING_LEVEL'] = os.environ.get('PYPI_PROXY_LOGGING_LEVEL',
                                                     'DEBUG')
        env_value = os.environ.get('PYPI_PROXY_PRIVATE_EGGS', None)
        if env_value:
            app.config['PRIVATE_EGGS'] = env_value.split(',')
        else:
            app.config['PRIVATE_EGGS'] = private_eggs

        app.config['PYPI_URL'] = os.environ.get('PYPI_PROXY_PYPI_URL',
                                                pypi_url)
        app.config['SHOULD_USE_EXISTING'] = os.environ.get(
                                            'PYPI_PROXY_SHOULD_USE_EXISTING',
                                            False)

    if not app.config['PYPI_URL'].endswith('/'):
        app.config['PYPI_URL'] = app.config['PYPI_URL'] + '/'


def configure_logging(app):
    ''' Setups the logging that will be used by the views to log the
    different problems that it might have.

    :param app: the application that will be used to register the URLs.
    '''
    if not app.debug:
        logging.basicConfig(filename=app.config['LOGGING_PATH'],
                            level=getattr(logging, app.config['LOGGING_LEVEL']),
                            format='%(asctime)s [%(levelname)s] %(message)s')

read_configuration(app)
configure_logging(app)
