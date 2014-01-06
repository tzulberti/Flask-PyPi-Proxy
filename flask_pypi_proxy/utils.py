# -*- coding: utf-8 -*-

from flask_pypi_proxy.app import app
from os.path import join
from hashlib import md5


def is_private(egg_name):
    ''' Checks if the egg_name is private or if belongs to one of
    the eggs that are uploaded to the normal pypi.

    :param str egg_name: the name of the egg without the version information.

    :return: true if the egg is private.
    '''
    return egg_name in app.config['PRIVATE_EGGS']


def get_base_path():
    ''' Gets the base path where all the eggs are on this servers
    '''
    return app.config['BASE_FOLDER_PATH']


def get_package_path(egg_name):
    ''' Given the name of a package, it gets the local path for it.

    :param egg_name: the name (it might also include the version) of
                     a python package.

    :return: the local path where the file can be found on the local
             system.
    '''
    return join(get_base_path(), egg_name)


def get_md5_for_content(package_content):
    ''' Given the content of a package it returns the md5 of the file.
    '''
    res = md5(package_content)
    return res.hexdigest()


def url_is_egg_file(url):
    return url is not None and (   url.lower().endswith('.zip')
                                or url.lower().endswith('.tar.gz')
                                or url.lower().endswith('.egg')
                                or url.lower().endswith('.exe')
                                or url.lower().endswith('.msi')
                                or url.lower().endswith('.whl'))
