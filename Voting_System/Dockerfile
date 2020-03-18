FROM ubuntu:18.04

RUN apt-get update -y && \
    apt-get install -y python-pip python-dev

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /Voting_System/requirements.txt

WORKDIR /Voting_System

EXPOSE 5000

RUN pip install -r requirements.txt

COPY . /Voting_System

ENTRYPOINT [ "python" ]

CMD [ "run.py" ]