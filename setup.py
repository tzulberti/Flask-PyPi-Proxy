from setuptools import setup, find_packages


setup(
    name='Flask-Pypi-Proxy',
    version='0.0.1',
    description='asd',
    long_description=open('README.rst').read(-1),
    author='Tomas Zulberti',
    author_email='tzulberti@gmail.com',
    license='BSD',
    url='https://github.com/tzulberti/unittest2-utils',
    install_requires=[
        "Flask",
        "requests",
        "python-magic",
    ],
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
)
