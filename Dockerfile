# Use the official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.9-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

# Install production dependencies.
RUN pip install Flask gunicorn
RUN pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app