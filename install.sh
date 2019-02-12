#!/usr/bin/env bash

#upgrade python installer:
python  -V
python -m pip install --upgrade pip
pip3 install --upgrade setuptools

#install libraries
pip install PySide2
#instal PySide2 from the developer branch
#revisar este merge para solucionar un problema https://github.com/pyqtgraph/pyqtgraph/pull/797/commits/aa8a61ba999eab836ff36a1c060351f4881ead9c
pip install numpy spicy matplotlib pywt