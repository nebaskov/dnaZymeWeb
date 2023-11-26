FROM python:3.10

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./database ./database
COPY ./dnaZymeWeb/ ./dnaZymeWeb
COPY ./main/ ./main
COPY ./prediction/ ./prediction
COPY ./requirements.txt .
COPY ./knowledgebase ./knowledgebase
COPY ./manage.py .

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/bin/bash", "-c", "python3 manage.py migrate --no-input && gunicorn dnaZymeWeb.wsgi:application --bind 0.0.0.0:8000"]
