FROM python:3.7-alpine

ENV PYTHONOPTIMIZE 1

COPY ./project /var/www/backend
COPY ./Pipfile* /var/www/backend/
COPY ./run.sh /var/www/backend/

WORKDIR /var/www/backend

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install pipenv \
    && pipenv sync

CMD ["sh", "run.sh"]