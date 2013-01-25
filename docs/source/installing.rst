=========
Deploying
=========

Flask-Pypi-Proxy is a normal Python Application, so it can be deployed
as any other Flask application. For more information, you can check here:

ASDASDA


Configuration
=============

The project uses the environment key **PYPI_PROXY_CONFIG_FILE** that references
the path where the configuration file is. This file is a YAML file with the
following keys:

:BASE_FOLDER_PATH:
    the base path where all the eggs will be stored. This is the base
    path. For example: /home/pypi/eggs. For each egg name, a subfolder
    will be created inside this folder. This value is required.

:PRIVATE_EGGS:
    a list with all the private eggs. On this eggs, Pypi won't be used
    and it will only answer from where take the data. By default, there
    are no private eggs, so everytime it will hit Pypi. This is usefull
    for private proyects, or for eggs that were uploaded after compilation
    (lxml, pil, etc...)

:PYPI_URL:
    the URL where from where the eggs should be downloaded. By default it
    uses: http://pypi.python.org. But I can be changed for any other.

If you don't want to use a configuration file, then environment variables
could be used. The environmental keys are the same as the one on the
configuration file, but they take the prefix: **PYPI_PROXY**. So the
environment keys used are:

* PYPI_PROXY_BASE_FOLDER_PATH
* PYPI_PROXY_PRIVATE_EGGS
* PYPI_PROXY_PYPI_URL

If the configuration file exists, then the values that are in the file
will be used and not the values of the system environment.