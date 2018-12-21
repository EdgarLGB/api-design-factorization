FROM frolvlad/alpine-python3

MAINTAINER Your Name "guobao1993.li@gmail.com"

COPY ./requirements.txt /application/requirements.txt

WORKDIR /application

RUN pip install -r requirements.txt

COPY . /application

CMD ["flask", "run", "--host=0.0.0.0"]