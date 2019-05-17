#<2019_hanium_project>/compose/Dockerfile
FROM python:3.6.5

RUN apt-get update
RUN mkdir /code
WORKDIR /code

#local requirements.txt => docker /code/
COPY requirements.txt /code/
RUN pip install -r /code/requirements.txt

#local => docker /code/
COPY . /code/
