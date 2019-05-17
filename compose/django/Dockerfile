#<2019_hanium_project>/compose/Dockerfile
FROM python:3.6.5

RUN apt-get update
RUN mkdir /code
WORKDIR /code

COPY requirements.txt /code/ #local requirements.txt => docker /code/
RUN pip install -r requirements.txt
COPY . /code/ #local => docker /code/
