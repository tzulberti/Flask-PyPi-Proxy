============
Introduction
============

Flask-Pypi-Proxy works is a proxy from Pypi that also enables you to upload
your custom packages.

Advantajes
==========

* Once that the package is downloaded from Pypi, then it won't be downloaded
  again. Bacause of this, the package instalation is quicker.
  Lets think that you have some servers where your application run.
  You configure one of this servers with Flask-Pypi-Proxy, and because of that
  all the servers download the required python packages from an internal server.

* You can upload you custom eggs. For example, you have your proyect which is
  close sourced and because of that it can't be uploaded to Pypi. This
  will solve the problem becuase you will have an internal package system.

* Uploaded compile packages. Some packages (lxml, Pillow) compile using the
  system libraries. If all the servers are using the same versions of the
  libraries, then you can upload the compiled package.

Disadvantajes
=============

* When downloading the package for the first time, it will take some extra time.
  This happens because the package will have to be downloaded from Pypi first,
  and then from the Flask-Pypi-Proxy

* There are some packages that fails to install them. For example: py-bcrypt.
  Basically, all the external packages that aren't hosted at pypi.python.org.
