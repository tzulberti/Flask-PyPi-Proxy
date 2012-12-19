# -*- coding: utf-8 -*-

from flask_pypi.app import app
from os.path import join
from hashlib import md5


def get_base_path():
    ''' Gets the base path where all the eggs are on this servers
    '''
    return app.config.get('BASE_FOLDER_PATH', '/tmp/pepe')


def get_package_path(egg_name):
    ''' Given the name of a package, it gets the local path for it.

    :param egg_name: the name (it might also include the version) of
                     a python package.

    :return: the local path where the file can be found on the local
             system.
    '''
    return join(get_base_path(), egg_name)


def get_url_for_package(egg_name):
    '''
    '''
    return '../../packages/sources/%s/%s/%s'


def get_md5_for_content(package_content):
    ''' Given the content of a package it returns the md5 of the file.
    '''
    res = md5(package_content)
    return res.hexdigest()
