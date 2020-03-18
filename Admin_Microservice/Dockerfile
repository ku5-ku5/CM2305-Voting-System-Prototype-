FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /Admin_Microservice/requirements.txt

WORKDIR /Admin_Microservice

RUN pip install -r requirements.txt

COPY . /Admin_Microservice

ENTRYPOINT [ "python" ]

CMD [ "wsgi.py" ]