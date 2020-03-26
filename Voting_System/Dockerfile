FROM python:3.6.8

LABEL Author="Rhys Connor"

ENV PYTHONDONTWRITEBYTECODE 1
ENV FLASK_APP "run.py"
ENV FLASK_ENV "development"
ENV FLASK_DEBUG True 

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /Voting_System/requirements.txt

WORKDIR /Voting_System

EXPOSE 5000
EXPOSE 3306

RUN pip install --upgrade pip
RUN pip install pipenv

RUN pip install -r requirements.txt

ADD . /Voting_System

CMD flask run --host=0.0.0.0