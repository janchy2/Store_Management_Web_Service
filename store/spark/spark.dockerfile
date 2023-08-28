FROM bde2020/spark-python-template:3.3.0-hadoop3.3

RUN apk add --update gcc musl-dev

RUN apk update && apk add --no-cache \
    build-base \
    python3-dev

RUN pip3 install greenlet flask_sqlalchemy==2.5.1

CMD [ "python3", "/app/ownerApplication.py" ]