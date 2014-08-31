=========
Deploying
=========

Flask-Pypi-Proxy is a normal Python application, so it can be deployed
as any other Flask application. For more information, you can check here:
`http://flask.pocoo.org/docs/deploying/ <http://flask.pocoo.org/docs/deploying/>`_


Configuration
=============

The project uses the environment key **FLASK_PYPI_PROXY_CONFIG** that references
the path where the configuration file is. This file is in JSON format with the
following keys:

BASE_FOLDER_PATH
    the base path where all the eggs will be stored. For example:
    /home/pypi/eggs. For each egg name, a subfolder will be created
    inside this folder. This value is required.

PRIVATE_EGGS
    a list with all the private eggs. For these eggs, PyPI won't be used
    and it will only answer with local data. By default, there
    are no private eggs, so everytime it will hit PyPI. This is useful
    for private projects, or for eggs that were uploaded after compilation
    (lxml, PIL, etc...)

PYPI_URL
    the URL where from where the eggs should be downloaded. By default it
    uses: http://pypi.python.org but it can be changed to any other. This might
    be useful, for example if you have a development/local proxy, that
    uses the production proxy.

LOGGING_PATH
    the complete filepath of the logging for the application. This file must
    include the path and the filename. This value is required.

LOGGING_LEVEL
    the string that represents the logging level that the application
    should use. In this case, it should be a string: DEBUG, INFO, WARNING,
    ERROR. By default, it uses DEBUG.

SHOULD_USE_EXISTING
    if True, then when getting the index for a package, ie the different
    versions, it will use the ones that exists on the local repo instead
    of using the information found on PYPI_URL. If False, and the package
    isn't private, then it will use the PYPI_URL to get the file package.
    Setting this value to True might do the things a little faster, but
    on the other hand, it might get you into trouble if trying to download
    a version of a package that doesn't exist, but other versions do exist.
    For example, you download version 1.4.2 of Django. If this value is
    set to True, then if you try to download version 1.5, it will return
    that it doesn't exist.

If you don't want to use a configuration file, then environment variables
could be used. The variable names are the same as the keys in the
configuration file, but they take the prefix: **PYPI_PROXY**. So the
variable names used are:

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


Debian/Ubuntu example installation
==================================

This is a **VERY** simple/basic configuration. It doesn't provide any
authentication, so this shouldn't be used on production.

.. code-block:: bash

    >>> sudo apt-get install apache2 libapache2-mod-wsgi
    >>> sudo apt-get install python-setuptools python-dev libxml2-dev libxslt-dev
    >>> sudo easy_install Flask-Pypi-Proxy

    >>> mkdir -p /mnt/eggs/
    >>> sudo chown www-data:www-data -R /mnt/eggs/

Now, lets create the WSGI configuration file (in this example, I will
create it on /mnt/eggs/flask_pypi_proxy.wsgi). The content of that file
will be something like:

.. code-block:: python

    import os

    os.environ['PYPI_PROXY_BASE_FOLDER_PATH'] = '/mnt/eggs/'
    os.environ['PYPI_PROXY_LOGGING_PATH'] = '/mnt/eggs/proxy.logs'

    # if installed inside a virtualenv, then do this:
    # activate_this = 'VIRTUALENENV_PATH/bin/activate_this.py'
    # execfile(activate_this, dict(__file__=activate_this))

    from flask_pypi_proxy.views import app as application

Finally, the Apache configuration. Create a file at
/etc/apache2/sites-enabled/flask_pypi_proxy with the following content:

::

    <VirtualHost *:80>
        WSGIDaemonProcess pypi_proxy threads=5
        WSGIScriptAlias / /mnt/eggs/flask_pypi_proxy.wsgi
    </VirtualHost>

Restart Apache

.. code-block:: bash

    >>> sudo service apache2 restart


More advanced configuration
===========================

The following steps will show you how to install this service inside a
virtualenv, also using HTTP basic auth to create some security for the eggs.

.. code-block:: bash

    >>> sudo apt-get install apache2 libapache2-mod-wsgi
    >>> sudo apt-get install python-setuptools python-dev libxml2-dev libxslt-dev

Now, create the user where the virtualenv will be installed:

.. code-block:: bash

    >>> sudo adduser pypi-proxy
    Adding user `pypi-proxy' ...
    Adding new group `pypi-proxy' (1001) ...
    Adding new user `pypi-proxy' (1001) with group `pypi-proxy' ...
    Creating home directory `/home/pypi-proxy' ...
    Copying files from `/etc/skel' ...
    Enter new UNIX password:
    Retype new UNIX password:
    >>> sudo easy_install virtualenv
    >>> sudo su - pypi-proxy

The following steps will be executed as **pypi-proxy**:

.. code-block:: bash

    mkdir ~/envs
    virtualenv ~/envs/proxy
    source ~/envs/proxy/bin/activate
    pip instal Flask-Pypi-Proxy
    mkdir /home/pypi-proxy/eggs/ # where the eggs will be
    chgrp www-data /home/pypi-proxy/eggs/
    chmod 775 /home/pypi-proxy/eggs/
    mkdir /home/pypi-proxy/logs/ # the same but for the logs files
    chgrp www-data /home/pypi-proxy/logs/
    chmod 775 /home/pypi-proxy/logs/

    htpasswd -c /home/pypi-proxy/htpasswd.file MY_USERNAME # creates the password file
    sudo chown www-data:www-data /home/pypi-proxy/htpasswd.file
    sudo chmod 620 /home/pypi-proxy/htpasswd.file

Under the same user, lets create the WSGI file (for this example, I will
put it on /home/pypi-proxy/pypi-proxy.wsgi). The content of this file is
as follows:

.. code-block:: python

    import os

    os.environ['PYPI_PROXY_BASE_FOLDER_PATH'] = '/home/pypi-proxy/eggs/'
    os.environ['PYPI_PROXY_LOGGING_PATH'] = '/home/pypi-proxy/logs/proxy.log'

    # if installed inside a virtualenv, then do this:
    activate_this = '/home/pypi-proxy/envs/proxy/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))

    from flask_pypi_proxy.views import app as application


Now return to the normal user, and create the following Apache configuration
(/etc/apache2/sites-enabled/flask_pypi_proxy):

::

    <VirtualHost *:80>
        <Location />
        AuthType Basic
        AuthUserFile /home/pypi-proxy/htpasswd.file
        AuthName "Private files"
        Require valid-user
        Order deny,allow
        Allow from all
        </Location>

        WSGIDaemonProcess pypi_proxy threads=5
        WSGIScriptAlias / /home/pypi-proxy/proxy.wsgi
    </VirtualHost>

Restart Apache

.. code-block:: bash

    sudo service apache2 restart
