#<2019_hanium_project>/compose/Dockerfile
FROM python:3.6.5

RUN apt-get update
RUN mkdir /code/
WORKDIR /code

#local requirements.txt => docker /code/
ADD . /code

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

