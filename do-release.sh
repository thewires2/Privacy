#!/bin/bash
python3 setup.py sdist bdist_wheel
twine check dist/*
twine upload --repository-url https://upload.pypi.org/legacy/ dist/*
