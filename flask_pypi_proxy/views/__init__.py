# -*- coding: utf-8 -*-

from flask_pypi_proxy.app import app
import flask_pypi_proxy.views.package
import flask_pypi_proxy.views.pypi
import flask_pypi_proxy.views.simple


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
