================
Flask-Pypi-Proxy
================

A pypi proxy done using flask. It will use Pypi, and then keep the downloaded
egg for future reference. After the package is downloaded from Pypi, it
won't download it from Pypi and use the local copy of the file.

How to use it
=============

To use it after the right configuration, you can use it by doing:

.. code-block:: bash

    pip install -i http://mypypiserver.com/simple/ <PACKAGE>


More documentation could be found here:
`https://flask-pypi-proxy.readthedocs.org/en/latest/index.html
<https://flask-pypi-proxy.readthedocs.org/en/latest/index.html>_`


Advantajes
==========

* Can have an local Pypi to download the eggs faster and doesn't depends on
  Pypi or any other service.

* Uploading your private python packages. This is usefull is you work for a
  company that have eggs, but doesn't open source them :(

* Uploading the compiled packages. There are some packages (lxml, Pillow) that
  are compiled each time that are installed. You can upload the compiled
  package to save some time.

* It does get newer versions. Supose that you installed Flask (0.8.0), and
  a new release is required. This is version 0.9. Then the new package will
  be downloaded from PyPi, and the proxy will be updated


Disadvantages
=============

* It doesn't seems to work with some packages.
