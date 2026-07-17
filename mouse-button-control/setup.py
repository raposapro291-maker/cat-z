#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="mouse-button-control",
    version="1.0.0",
    author="raposapro291-maker",
    author_email="raposapro291@gmail.com",
    description="Advanced mouse button customization application for Linux",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/raposapro291-maker/cat-z",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Desktop Environment",
        "Environment :: X11 Applications :: Qt",
    ],
    python_requires=">=3.12",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "mouse-button-control=mouse_button_control.main:main",
        ],
    },
    include_package_data=True,
)
