FROM python:3.10-alpine


WORKDIR /app

RUN apk update 

RUN apk add --no-cache gcc
RUN apk add --no-cache libc-dev
RUN apk add --no-cache libffi-dev
RUN apk add --no-cache git

RUN pip3 install poetry

COPY pyproject.toml /app 

RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD} 



CMD [ "poetry", "run", "python", "main.py" ]