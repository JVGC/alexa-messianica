#Install poetry
pip install poetry

#Install dependencies
poetry config virtualenvs.create false && poetry install

#Install scrapy
pip3 install wheel scrapy