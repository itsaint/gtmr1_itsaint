from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name = "gtmr1_itsaint",
    version = "1.0.5",
    author = "Santosh T",
    author_email = "itsaint@gmail.com",
    description = "Geektrust Challenge Make Room",
    long_description= long_description,
    long_description_content_type="text/markdown",
    package_dir = {"":"."},
    py_modules = ["geektrust" , "msl.scheduler"],
    url = "https://github.com/itsaint/gtmr1_itsaint",
    project_urls={
        "Bug Tracker": "https://github.com/itsaint/gtmr1_itsaint/issues",
    },
    classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],
    package_data={ "" : ["config.json"] }

)
