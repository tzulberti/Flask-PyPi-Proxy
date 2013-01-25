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

Uploading packages
==================



