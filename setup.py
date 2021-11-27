from setuptools import setup


setup(
    name = "gtms1_itsaint",
    version = "0.0.1",
    author = "Santosh T",
    author_email = "itsaint@gmail.com",
    description = "Geektrust Challenge Make Room",
    package_dir = {"":"src"},
    py_modules = ["geektrust" , "msl.scheduler"]
)

'''
    install_requires=[
        'sortedcontainers',
    ],
author = Santosh T
author_email = itsaint@gmail.com
description = Geektrust Challenge Make Room
long_description = file: README.md
long_description_content_type = text/markdown
url = https://github.com/itsaint/gtmr1_itsaint
project_urls =
    Bug Tracker = https://github.com/itsaint/gtmr1_itsaint/issues
classifiers =
    Programming Language :: Python :: 3
    License :: OSI Approved :: MIT License
    Operating System :: OS Independent

[options]
py_modules = geektrust ,
package_dir =
    = src
packages = find:
python_requires = >=3.8

[options.packages.find]
where = src
'''