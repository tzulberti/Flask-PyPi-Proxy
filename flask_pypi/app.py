# -*- coding: utf-8 -*-

''' The main Flask application which take care of reading the configuration.
'''

from flask import Flask

app = Flask(__name__)
app.config['PRIVATE_EGGS'] = []
