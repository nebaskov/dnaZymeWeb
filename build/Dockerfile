from python:3.10

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# ENV POETRY_VERSION 1.6.1

COPY ./database .
COPY ./dnaZymeWeb .
COPY ./main .
COPY ./prediction .
COPY ./requirements.txt .
COPY ./manage.py .
COPY ./pyproject.toml .
COPY ./poetry.lock .

# RUN pip install poetry==${POETRY_VERSION}

# RUN poetry config virtualenvs.create false

# RUN poetry install --no-interaction

RUN pip3 install -r requirements.txt

ENTRYPOINT ["/bin/bash", "-c", "python3 manage.py migrate --no-input && gunicorn dnaZymeWeb.wsgi:application --bind 0.0.0.0:8000"]
