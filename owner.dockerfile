FROM python:3

RUN mkdir -p /opt/src/store
WORKDIR /opt/src/store

COPY store/ownerApplication.py ./ownerApplication.py
COPY store/configuration.py ./configuration.py
COPY store/models.py ./models.py
COPY store/requirements.txt ./requirements.txt
COPY store/decorators.py ./decorators.py

RUN pip install -r ./requirements.txt

ENV PYTHONPATH="/opt/src/store"

ENTRYPOINT ["python", "./ownerApplication.py"]