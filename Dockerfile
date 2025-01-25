FROM python:3.12.2-alpine3.19

ENV APP_HOME /application

WORKDIR $APP_HOME

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml ./

RUN pip install poetry && \
    poetry install --no-root --no-interaction

COPY . .

RUN chmod u+x entrypoint.sh

ENTRYPOINT ["./entrypoint.sh"]
