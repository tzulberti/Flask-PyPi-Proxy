===============
Using the proxy
===============


Downloading packages
====================

To download a package from the proxy, there are two choices:

* Specify the server where the server is installed when runing **pip** or
  **easy_install**.

  .. code-block:: bash

      pip install -i http://mypypiproxy/simple/ Flask
      easy_install -i http://mypypiproxy/simple/ Flask

* Use the index url in a configuration file. For easy_install, it
  should be on **~/.pydistutils.cfg** (on Linux), and the file should have
  the following format::

    [easy_install]
    index_url = http://mypypiproxy/simple/

  For **pip**, the configuration file is **~/.pip/pip.conf**, and the file
  should have the following format::

    [global]
    index-url = http://mypypiproxy/simple/

Also, you should increment the timeout option for **pip** or **easy_install**.
For pip, the **~/.pip/pip.conf** configuration file should be something like:

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

I you are using the configuration with basic auth, then the configuration
file should look something like this:

.. code-block::

    [distutils]
    index-servers =
        miserver

    [myserver]
    username:basicauth_username
    password:basciauth_password
    repository:http://mypypiproxy/pypi/

Basically, you should put in the username and password used for the basic auth.

The username and password values aren't required by Flask-Pypi-Proxy.
They are used by distutils when uploading the package. If you don't have
any authentication after this, then you can put any values. After that,
go to the **setup.py** of your project and run:

.. code-block:: bash

    python setup.py sdist upload -r myserver

**IMPORTANT:** The command *register*, won't work if you are using basic auth.
For example, if you run

.. code-block:: bash

    python setup.py register

and if your server is configured using basic auth, then register will return
a 401 error. Simply upload the package without running register.
