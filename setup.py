from setuptools import setup


setup(
    name="vedirect",
    version="1.1.0",
    author="Frank Villaro-Dixon",
    author_email="frank@villaro-dixon.eu",
    description=("Interfaces with Victron VE.Direct devices"),
    license="MIT",
    keywords="victron vedirect ve.direct ve direct mppt",
    url="http://github.com/Frankkkkk/python-vedirect",
    py_modules=['vedirect'],
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    install_requires=['pyserial'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
    ],
)
