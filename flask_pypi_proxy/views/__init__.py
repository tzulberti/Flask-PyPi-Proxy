# -*- coding: utf-8 -*-

from flask_pypi.app import app
import flask_pypi.views.package
import flask_pypi.views.pypi
import flask_pypi.views.simple


if __name__ == '__main__':
    app.run(debug=True)
