#!/bin/bash

#Install poetry
curl -sSL https://install.python-poetry.org | python3 -

export PATH="/home/ubuntu/.local/bin:$PATH"

#Install dependencies
poetry install

#Install scrapy
pip3 install wheel scrapy