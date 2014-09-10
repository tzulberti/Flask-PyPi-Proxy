================
Flask-Pypi-Proxy
================

A PyPI proxy done using Flask. It will use PyPI, and then keep the downloaded
egg for future reference. After the package is downloaded from PyPI, it
won't download it from PyPI again and instead use the local copy of the file.

How to use it
=============

To use it after the right configuration, run:

.. code-block:: bash

    pip install -i http://mypypiserver.com/simple/ <PACKAGE>


Documentation can be found here:
`https://flask-pypi-proxy.readthedocs.org/en/latest/index.html
<https://flask-pypi-proxy.readthedocs.org/en/latest/index.html>`_.


Advantages
==========

* A local PyPI mirror to download the eggs faster and doesn't depends on
  PyPI or any other service.

* Uploading your private python packages. This is useful if you work for a
  company that have eggs, but doesn't open source them :(

* Uploading the compiled packages. There are some packages (lxml, Pillow) that
  are compiled each time that are installed. You can upload the compiled
  package to save some time.

* It does get newer versions. Supose that you installed Flask (0.8.0), and
  a new release is required. This is version 0.9. Then the new package will
  be downloaded from PyPI, and the proxy will be updated.


Special Thanks
==============

Special thanks to `robin-jarry <https://github.com/robin-jarry>`_,
`jokull <https://github.com/jokull>`_,
`michaelmior <https://github.com/michaelmior>`_ and to
`Tenzer <https://github.com/Tenzer>`_.
