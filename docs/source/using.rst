===============
Using the proxy
===============


Downloading packages
====================

To download a package from the proxy, there are two choices:

* To specify the server where the server is installed when runing **pip** or
  **easy_install**.

  .. code-block:: bash

      pip install -i http://mypypiproxy/simple/ Flask
      easy_install -i http://mypypiproxy/simple/ Flask

* To use the index url in a configuration file. For easy_install, it
  should be on **~/.pydistutils.cfg** (on linux), and the file should have
  the following format::

    [easy_install]
    index_url = http://mypypiproxy/simple/

  For **pip**, the configuration file is **.pip/pip.conf**, and the file
  should have the following format::

    [global]
    index-url = http://mypypiproxy/simple/

Also, you should increment the timeout option for **pip** or **easy_install**.
For pip, the **.pip/pip.conf** configuration file should be something like::

    [global]
    index-url = http://mypypiproxy/simple/
    timeout = 60


Uploading packages
==================

To upload a package, the **~/.pypirc** should be updated to something
like:

.. code-block:: ini

    [distutils]
    index-servers =
        miserver

    [myserver]
    username:foo
    password:bar
    repository:http://mypypiproxy/pypi/

I you are using the configuration with Basic Auth, then the configuration
file should look something like this:

.. code-block::

    [distutils]
    index-servers =
        miserver

    [myserver]
    username:basicauth_username
    password:basciauth_password
    repository:http://mypypiproxy/pypi/

Basically, you should put on the username and password configuration values
the username and password used for the Basic Auth.

The username and password values aren't required by the Flask-Pypi-Proxy.
They are used by distutils when uploading the package. If you don't have
any authentification after this, then you can put any values. After that,
go to the **setup.py** of your project and run:

.. code-block:: bash

    python setup.py sdist upload -r myserver

**IMPORTANT:** the comand *register*, won't work if you are using Basic Auth
For example, if you run

.. code-block:: bash

    python setup.py register

and your server is configured using Basic Auth, then the register will return
a 401 error. Simply upload the package without running the register

