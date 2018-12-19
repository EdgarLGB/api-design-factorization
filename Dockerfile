FROM ubuntu:18.10

MAINTAINER Your Name "guobao1993.li@gmail.com"

RUN apt-get update
RUN apt-get install -y python3 python3-dev python3-pip nginx
RUN pip3 install uwsgi

COPY ./requirements.txt /application/requirements.txt

WORKDIR /application

RUN pip3 install -r requirements.txt

COPY . /application

CMD ["python3", "app/app.py"]