FROM python:3.11.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /Articles

COPY Pipfile Pipfile.lock /Articles/
RUN pip install pipenv && pipenv install --system

COPY . /Articles/