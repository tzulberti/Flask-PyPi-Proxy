============
Introduction
============

Flask-Pypi-Proxy works is a proxy for PyPI that also enables you to upload
your custom packages.

Advantages
==========

* Once a package is downloaded from PyPI, then it won't be downloaded
  again. Bacause of this, the package installation is quicker.
  Let's assume that you have some servers where your application run.
  You configure one of these servers with Flask-Pypi-Proxy, and because of that
  all the servers download the required Python packages from an internal server.

* You can upload your custom eggs. For example, you have your project which is
  close sourced and because of that it can't be uploaded to PyPI. This
  will solve the problem because you will have an internal package system.

* Upload compiled packages. Some packages (lxml, Pillow) compile using the
  system libraries. If all the servers are using the same versions of the
  libraries, then you can upload the compiled package and save the compilation
  time for each install.

Disadvantages
=============

* When downloading the package for the first time, it will take some extra time.
  This happens because the package will have to be downloaded from PyPI first,
  and then from the Flask-Pypi-Proxy.
