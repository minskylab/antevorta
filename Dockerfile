FROM python:3.10-alpine

WORKDIR /app

RUN apk update 

RUN apk add --no-cache gcc
RUN apk add --no-cache libc-dev
RUN apk add --no-cache libffi-dev
RUN apk add --no-cache git
RUN apk add build-base
# RUN apt-get install -y build-essential
RUN pip3 install poetry

COPY pyproject.toml /app 

RUN pip install --upgrade "pip>=20.3"
RUN pip install --upgrade orjson

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . /app

# ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

CMD [ "poetry", "run", "python", "main.py" ]