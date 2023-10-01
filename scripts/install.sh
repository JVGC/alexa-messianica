#install a python virtual environment
python3 -m venv python_env

#activate the python virtual environment
source python_env/bin/activate
pip install poetry

#install any python modules specified in the requirements.txt file
poetry config virtualenvs.create false && poetry install

#install scrapy
pip3 install wheel scrapy