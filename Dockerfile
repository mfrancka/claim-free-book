FROM python:3.8-alpine

RUN mkdir /app
COPY Pipfile /app/Pipfile
COPY Pipfile.lock /app/Pipfile.lock
COPY free.py /app/free.py
RUN pip install pipenv
WORKDIR /app
RUN pipenv install --deploy

ENTRYPOINT ["pipenv", "run", "python3", "/app/free.py"]