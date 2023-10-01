#Install poetry
curl -sSL https://install.python-poetry.org | python3 -

#Install dependencies
poetry config virtualenvs.create false && poetry install

#Install scrapy
pip3 install wheel scrapy