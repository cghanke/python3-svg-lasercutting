from setuptools import setup
from os import path, environ
from sys import argv

here = path.abspath(path.dirname(__file__))

try:
    if argv[1] == "test":
        environ['PYTHONPATH'] = here
except IndexError:
    pass

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='svgwrite_laser',
    version='0.1',
    description='Extensions to svgwrite for lasercutting',
    long_description=long_description,
    author='Christof Hanke',
    author_email='christof.hanke@induhviduals.de',
    url='https://github.com/ya-induhvidual/python3-svg-lasercutting',
    packages=['svgwrite_laser'],
    license='MIT',
    install_requires=['svgwrite'],
    test_suite="test/test_all.py",
    keywords='svg laser',
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: POSIX :: BSD :: FreeBSD',
        'Operating System :: POSIX :: Linux',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Intended Audience :: End Users/Desktop',
    ],
)

