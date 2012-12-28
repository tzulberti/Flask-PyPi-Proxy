# -*- coding: utf-8 -*-

''' Handles downloading a package file.

This is called by easy_install or pip after calling the simple, and getting
the version of the package to download.

'''

import magic
from flask import make_response, request, abort
from flask_pypi.app import app
from flask_pypi.utils import (get_base_path, get_package_path,
                              get_md5_for_content)
from os import makedirs
from os.path import join, exists
from requests import get, head
# from subprocess import Popen


@app.route('/packages/source/<source_letter>/<package_name>/<package_file>',
           methods=['GET', 'HEAD'])
def package(source_letter, package_name, package_file):
    egg_filename = join(get_base_path(), package_name, package_file)
    if request.method == 'HEAD':
        if not exists(egg_filename):
            url = 'http://pypi.python.org/packages/source/%s/%s/%s' % (
                        source_letter, package_name, package_file)
            pypi_response = head(url)
            return _respond(pypi_response.content, pypi_response.headers['content-type'])

        else:
            mimetype = magic.from_file(egg_filename, mime=True)
            return _respond('', mimetype)

    if exists(egg_filename):
        # entonces tengo que leer el contenido del archivo y pasarselo
        path = get_package_path(package_name)
        path = join(path, package_file)
        with open(path, 'rb') as egg:
            content = egg.read(-1)
        mimetype = magic.from_file(egg_filename, mime=True)
        return _respond(content, mimetype)

    else:
        # TODO: aca tengo ciertos problemas si bajo el paquete a mano.
        # tengo que usar pip porque con ciertos paquetes no tengo ni
        # idea de como es que realmente los baja
        # por ejemplo: py-bcrypt
        package_path = get_package_path(package_name)
        pypi_response = get('http://pypi.python.org/packages/source/%s/%s/%s' % (
                                source_letter, package_name, package_file
                           ))

        if pypi_response.status_code != 200:
            abort(pypi_response.status_code)

        if not exists(package_path):
            makedirs(package_path)

        with open(egg_filename, 'w') as egg_file:
            egg_file.write(pypi_response.content)

        #
        # print ' '.join(['pip', 'install', '-d', package_path, package_file])
        # pip_process = Popen(['pip', 'install', '-d', package_path, package_file])
        # pip_process.wait()

        # if pip_process.returncode != 0:
        #     # todo aca se deberia borrar la carpeta creada anteriormente
        #     pass

        with open(egg_filename) as egg_file:
            filecontent = egg_file.read(-1)
            mimetype = magic.from_file(egg_filename, mime=True)

        with open(egg_filename + '.md5', 'w') as md5_output:
            md5 = get_md5_for_content(filecontent)
            md5_output.write(md5)

        return _respond(filecontent, mimetype)


def _respond(filecontent, mimetype):
    return make_response(filecontent, 200, {
                        'Content-Type': mimetype
                    }
            )
