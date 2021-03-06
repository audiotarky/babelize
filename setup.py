# -*- coding: utf-8; mode:python -*-

import pathlib

from setuptools import find_packages, setup

here = pathlib.Path(__file__).parent.resolve()

long_description = (here / "README.md").read_text(encoding="utf-8")

setup(
    name="babelize",
    version="0.0.1",
    description="A translation framework for Hugo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/audiotarky/babelize",
    author="Audiotarky",
    author_email="author@audiotarky.com",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(where="babelize"),
    python_requires=">=3.6, <4",
    entry_points={
        "console_scripts": [
            "babelize=babelize.main:main",
        ],
    },
)
