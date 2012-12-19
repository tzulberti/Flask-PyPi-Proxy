# -*- coding: utf-8 -*-

from collections import namedtuple
from os import listdir
from os.path import join, exists, split

from flask import abort, render_template
from pyquery import PyQuery
from requests import get

from flask_pypi.app import app
from flask_pypi.utils import get_package_path, get_base_path


VersionData = namedtuple('VersionData', ['name', 'md5'])


@app.route('/simple/')
def simple():
    packages = []
    for filename in listdir(get_base_path()):
        packages.append(filename)
    return render_template('simple.html', packages=packages)


@app.route('/simple/<package_name>/')
def simple_package(package_name):
    package_folder = get_package_path(package_name)
    if exists(package_folder):
        package_versions = []
        template_data = dict(
            source_letter=package_name[0],
            package_name=package_name,
            versions=package_versions
        )

        for filename in listdir(package_folder):
            if not filename.endswith('.md5'):
                # entonces es un archivo EGG por lo que no tiene
                # sentido que lo tenga en cuenta porque lo voy a tener
                # en cuenta por el md5
                continue

            with open(join(package_folder, filename)) as md5_file:
                md5 = md5_file.read(-1)

            # remove .md5 extension
            name = filename[:-4]
            data = VersionData(name, md5)
            package_versions.append(data)

        return render_template('simple_package.html', **template_data)
    else:
        url = 'http://pypi.python.org/simple/%s' % package_name
        print "Simple: %s" % url
        response = get(url)
        print "Finished simple"
        if response.status_code != 200:
            abort(response.status_code)
        # TODO falta grabarlo localmente
        content = response.content
        p = PyQuery(content)
        for anchor in p("a"):
            foo = PyQuery(anchor)
            href = foo.attr("href")
            if not href.startswith('../../packages/source'):
                # then the link is to an external server.
                # I will change it so it references the local server
                # and this proxy has the values from that server.

                # For example:
                #   view-source:http://pypi.python.org/simple/nose/
                # the lastest versions references somethingaboutrange.com
                # and because of that PIP won't use this proxy
                package_version = split(href)[-1]
                corrected_href = '../../packages/source/%s/%s/%s' % (
                        package_name[0],
                        package_name,
                        package_version
                )
                foo.attr("href", corrected_href)
        content = p.outerHtml()
        return content
