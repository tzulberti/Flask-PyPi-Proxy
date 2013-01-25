# -*- coding: utf-8 -*-


'''Gets the list of the packages that can be downloaded.

'''

from collections import namedtuple
from os import listdir
from os.path import join, exists, split

from flask import abort, render_template
from pyquery import PyQuery
from requests import get

from flask_pypi_proxy.app import app
from flask_pypi_proxy.utils import get_package_path, get_base_path, is_private


VersionData = namedtuple('VersionData', ['name', 'md5'])


@app.route('/simple/')
def simple():
    ''' Return the template which list all the packages that are installed
    '''
    packages = []
    for filename in listdir(get_base_path()):
        packages.append(filename)
    return render_template('simple.html', packages=packages)


@app.route('/simple/<package_name>/')
def simple_package(package_name):
    ''' Given a package name, returns all the versions for downloading
    that package.

    If the package doesn't exists, then it will call PyPi (CheeseShop).
    But if the package exists in the local path, then it will get all
    the versions for the local package.

    This will take into account if the egg is private or if it is a normal
    egg that was uploaded to PyPi. This is important to take into account
    the version of the eggs. For example, a proyect requires request==1.0.4
    and another package uses request==1.0.3. Then the instalation of the
    second package will fail because it wasn't downloaded an the **request**
    folder only has the 1.0.4 version.

    To solve this problem, the system uses 2 different kinds of eggs:

    * private eggs: are the eggs that you uploaded to the private repo.
    * normal eggs: are the eggs that are downloaded from pypi.

    So the normal eggs will always get the simple page from the pypi repo,
    will the private eggs will always be read from the filesystem.


    :param package_name: the name of the egg package. This is only the
                          name of the package with the version or anything
                          else.

    :return: a template with all the links to download the packages.
    '''

    package_folder = get_package_path(package_name)
    if is_private(package_name) and exists(package_folder):
        package_versions = []
        template_data = dict(
            source_letter=package_name[0],
            package_name=package_name,
            versions=package_versions
        )

        for filename in listdir(package_folder):
            if not filename.endswith('.md5'):
                # I only read .md5 files so I skip this egg (or tar,
                # or zip) file
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
        response = get(url)
        if response.status_code != 200:
            abort(response.status_code)

        content = response.content
        p = PyQuery(content)
        for anchor in p("a"):
            panchor = PyQuery(anchor)
            href = panchor.attr("href")
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
                panchor.attr("href", corrected_href)
        content = p.outerHtml()
        return content
