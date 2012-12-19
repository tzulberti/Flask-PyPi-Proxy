# -*- coding: utf-8 -*-

from flask import abort
from flask_pypi.app import app
from flask_pypi.utils import (get_base_path, get_package_path,
                              get_md5_for_content)
from os import makedirs
from os.path import join, exists
from requests import get


@app.route('/packages/source/<source_letter>/<package_name>/<package_file>',
           methods=['GET'])
def package(source_letter, package_name, package_file):
    egg_file = join(get_base_path(), package_name, package_file)
    if exists(egg_file):
        # entonces tengo que leer el contenido del archivo y pasarselo
        path = get_package_path(package_name)
        path = join(path, package_file)
        with open(path, 'rb') as egg:
            content = egg.read(-1)
        return content
    else:
        url = 'http://pypi.python.org/packages/source/%s/%s/%s' % (
                        source_letter, package_name, package_file)
        print "Url: %s" % url
        response = get(url)
        package_path = get_package_path(package_name)
        if not exists(package_path):
            makedirs(package_path)

        if response.status_code != 200:
            abort(response.status_code)

        print "Finish downloading file..."
        with open(egg_file, 'wb') as output:
            output.write(response.content)

        with open(egg_file + '.md5', 'w') as md5_output:
            md5 = get_md5_for_content(response.content)
            md5_output.write(md5)
        return response.content


@app.route('/packages/source/<source_letter>/<package_name>/<package_file>',
            methods=['HEAD'])
def check_existance(source_letter, package_name, package_file):
    egg_file = join(get_base_path(), package_name, package_file)
    if exists(egg_file):
        return '', 200
    else:
        abort(404)
