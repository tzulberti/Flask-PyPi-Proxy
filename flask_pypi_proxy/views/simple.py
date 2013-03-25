# -*- coding: utf-8 -*-


''' Gets the list of the packages that can be downloaded.
'''

import urllib
import urlparse
from collections import namedtuple
from os import listdir
from os.path import join, exists, basename

from flask import abort, render_template
from pyquery import PyQuery
from requests import get

from flask_pypi_proxy.app import app
from flask_pypi_proxy.utils import get_package_path, get_base_path, is_private, url_is_egg_file


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
    app.logger.debug('Requesting index for: %s', package_name)
    package_folder = get_package_path(package_name)
    if (is_private(package_name) or (
            exists(package_name) and app.config['SHOULD_USE_EXISTING'])):

        app.logger.debug('Found information of package: %s in local repository',
                         package_name)
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
        app.logger.debug('Didnt found package: %s in local repository. '
                         'Using proxy.', package_name)
        url = app.config['PYPI_URL'] + 'simple/%s' % package_name
        response = get(url)
        if response.status_code != 200:
            app.logger.warning('Error while getting proxy info for: %s'
                               'Errors details: %s', package_name,
                               response.text)
            abort(response.status_code)

        content = response.content
        p = PyQuery(content)
        external_links = set()
        for anchor in p("a"):
            panchor = PyQuery(anchor)
            href = panchor.attr('href')
            # robin-jarry: modified the href to ../../packages/
            # so that it works also for non-source packages (.egg, .exe and .msi)
            parsed = urlparse.urlparse(href)
            
            if parsed.hostname:
                # the link is to an external server.
                if parsed.hostname == 'pypi.python.org':
                    # we remove the hostname to make the URL relative
                    panchor.attr('href', parsed.path)
                else:
                    if panchor.attr('rel') == 'download':
                        if url_is_egg_file(parsed.path):
                            # href points to a filename
                            external_links.add('<a href="%s">%s</a>' % (href, basename(parsed.path)))
                        else:
                            # href points to an external page where we will find 
                            # links to package files
                            external_links.update(find_external_links(app, href))
                    # what ever happens, we remove the link for now
                    # we'll add the external_links after that we found after
                    panchor.remove()                    
            else:
                # local link to pypi.python.org
                if not href.startswith('../../packages/'):
                    # ignore anything else than package links
                    panchor.remove()
            
        # after collecting all external links, we insert them in the html page
        for link in external_links:
            plink = PyQuery(link)
            href = plink.attr('href')
            plink.attr('href', convert_to_internal_url(href, package_name, basename(href)))
            p('a').after(plink)
        
        content = p.outerHtml()
        return content


def find_external_links(app, url):
    '''Look for links to files in a web page and returns a set.
    '''
    links = set()
    response = get(url)
    if response.status_code != 200:
        app.logger.warning('Error while getting proxy info for: %s'
                           'Errors details: %s', url,
                           response.text)
    else:
        if response.content:
            p = PyQuery(response.content)
            for anchor in p("a"):
                panchor = PyQuery(anchor)
                href = panchor.attr("href")
                if url_is_egg_file(href):
                    # href points to a filename
                    href = get_absolute_url(href, url)
                    links.add('<a href="%s">%s</a>' % (href, panchor.text()))
    return links


def get_absolute_url(url, root_url):
    '''Make relative URLs absolute
    
    >>> get_absolute_url('/src/blah.zip', 'https://awesome.org/')
    'https://awesome.org/src/blah.zip'
    >>> get_absolute_url('http://foo.bar.org/blah.zip', 'https://awesome.org/')
    'http://foo.bar.org/blah.zip'
    '''
    parsed = urlparse.urlparse(url)
    if parsed.scheme:
        return url
    else:
        return urlparse.urljoin(root_url, parsed.path)
    

def convert_to_internal_url(external_url, package_name, filename):
    '''Convert an external URL (i.e. not on pypi.python.org) to something 
    that can be sent to the clients behind our proxy.
    
    Example:
    
    >>> convert_to_internal_url('http://foo.bar.org/src/blah-1.2.zip', 'blah', 'blah-1.2.zip')
    '../../packages/external/b/blah/blah-1.2.zip?remote=http%3A%2F%2Ffoo.bar.org%2Fsrc%2Fblah-1.2.zip'
    '''
    return '../../packages/external/%s/%s/%s?%s' % (package_name[0],
                                                    package_name,
                                                    filename,
                                                    urllib.urlencode({'remote': external_url}))
