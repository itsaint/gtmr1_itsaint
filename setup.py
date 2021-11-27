from setuptools import setup


setup(
    name = "gtmr1_itsaint",
    version = "1.0.0",
    author = "Santosh T",
    author_email = "itsaint@gmail.com",
    description = "Geektrust Challenge Make Room",
    package_dir = {"":"src"},
    py_modules = ["geektrust" , "msl.scheduler"],
    url = "https://github.com/itsaint/gtmr1_itsaint",
    classifiers=[
                "Programming Language :: Python :: 3",
                "License :: OSI Approved :: MIT License",
                "Operating System :: OS Independent",
            ],
    package_data={ "" : ["config.json"] }

)
