FROM python:buster

RUN apt update -y
RUN apt install -y netcat

WORKDIR /app

COPY ./app/requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY app .
COPY data /data

CMD ["python3", "run.py"]
