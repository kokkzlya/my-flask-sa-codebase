# My Flask-SA Codebase

## Prerequisites
1. python 3.11 or later
1. pyenv
1. poetry
1. Docker

## How to run
1. Run `pyenv shell <your_python_version>`, for example: `pyenv shell 3.11.4`
1. ```./bootstrap```
1. ```./manage run_dev```
1. ```curl -i -X GET http://myproject.127.0.0.1.nip.io:5000/```

## How to add or modify table
1. Add class or modify the attribute of the class in `src/myproject/repository/model.py`
1. ```poetry run alembic revision -m "my revision" --autogenerate```
1. ```./bootstrap```
