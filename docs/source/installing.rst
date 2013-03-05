=========
Deploying
=========

Flask-Pypi-Proxy is a normal Python Application, so it can be deployed
as any other Flask application. For more information, you can check here:
`http://flask.pocoo.org/docs/deploying/ <http://flask.pocoo.org/docs/deploying/>`_


Configuration
=============

The project uses the environment key **PYPI_PROXY_CONFIG_FILE** that references
the path where the configuration file is. This file is a JSON file with the
following keys:

BASE_FOLDER_PATH
    the base path where all the eggs will be stored. This is the base
    path. For example: /home/pypi/eggs. For each egg name, a subfolder
    will be created inside this folder. This value is required.

PRIVATE_EGGS
    a list with all the private eggs. On this eggs, Pypi won't be used
    and it will only answer from where take the data. By default, there
    are no private eggs, so everytime it will hit Pypi. This is usefull
    for private proyects, or for eggs that were uploaded after compilation
    (lxml, pil, etc...)

PYPI_URL
    the URL where from where the eggs should be downloaded. By default it
    uses: http://pypi.python.org. But I can be changed for any other. This might
    be usefull, for example if you have a development/local proxy, that
    uses the production proxy.

LOGGING_PATH
    the complete filepath of the logging for the aplication. This file must
    include the path and the filename. This value is required

LOGGING_LEVEL
    the string that represents the logging level that the application
    should use. In this case, it should be an string: DEBUG, INFO, WARNING,
    ERROR. By default, it uses DEBUG.

SHOULD_USE_EXISTING
    if True, then when getting the index for a package, ie the different
    versions, it will use the ones that exists on the local repo instead
    of using the information found on PYPI_URL. If False, and the package
    isn't private, then it will use the PYPI_URL to get the file package.
    Setting this value to True, migth do the things a litter faster, but
    on the other hand, it might get intro trouble if trying to download
    a version of a package that doesn't exists, but other version does exists.
    For example, you download version 1.4.2 of Django. If this value is
    set to True, then if you try to download version 1.5, it will return
    that it doesn't exists.

If you don't want to use a configuration file, then environment variables
could be used. The environmental keys are the same as the one on the
configuration file, but they take the prefix: **PYPI_PROXY**. So the
environment keys used are:

* PYPI_PROXY_BASE_FOLDER_PATH
* PYPI_PROXY_LOGGING_PATH
* PYPI_PROXY_LOGGING_LEVEL
* PYPI_PROXY_PRIVATE_EGGS
* PYPI_PROXY_PYPI_URL
* PYPI_PROXY_SHOULD_USE_EXISTING

If the configuration file exists, then the values that are in the file
will be used and not the values of the system environment.

An example of the file could be:

.. code-block:: json

    {
        BASE_FOLDER_PATH: '/mnt/eggs/',
        LOGGING_PATH: '/mnt/eggs/debug.log',
        PRIVATE_EGGS: [
            'miproject1',
            'miproject2',
            'miproject3'
            ],
        PYPI_URL: 'https://pypy.miserver.com'
    }

But a more common configuration file, will be:

.. code-block:: json

    {
        BASE_FOLDER_PATH: '/mnt/eggs/',
        LOGGING_PATH: '/mnt/eggs/debug.log',
    }


Debian/Ubuntu Example Instalation
=================================

This is a **VERY** simple/basic configuration. It doesn't provide any
authentification, so this shouldn't be used on production.

.. code-block:: bash

    >>> sudo apt-get install apache2 libapache2-mod-wsgi
    >>> sudo apt-get install python-setuptools python-dev libxml2-dev libxslt-dev
    >>> sudo easy_install Flask-Pypi-Proxy

    >>> mkdir -p /mnt/eggs/
    >>> sudo chown www-data:www-data -R /mnt/eggs/

    >>> cat /mnt/eggs/flask_pypi_proxy.wsgi
    import os

    os.environ['PYPI_PROXY_BASE_FOLDER_PATH'] = '/mnt/eggs/'
    os.environ['PYPI_PROXY_LOGGING_PATH'] = '/mnt/eggs/proxy.logs'

    # if installed inside a virtualenv, then do this:
    # activate_this = 'VIRTUALENENV_PATH/bin/activate_this.py'
    # execfile(activate_this, dict(__file__=activate_this))

    from flask_pypi_proxy.views import app as application

    >>> cat /etc/apache2/sites-enabled/flask_pypi_proxy
    <VirtualHost *:80>
        WSGIDaemonProcess pypi_proxy threads=5
        WSGIScriptAlias / /mnt/eggs/flask_pypi_proxy.wsgi
    </VirtualHost>




