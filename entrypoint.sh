#!/bin/sh

poetry run alembic -c application/alembic.ini upgrade head

poetry run python run.py