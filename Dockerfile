FROM python:3.7-alpine

RUN mkdir /app
COPY requirements.txt /app/requirements.txt
COPY free.py /app/free.py
RUN pip install -r /app/requirements.txt

ENTRYPOINT ["python3", "/app/free.py"]