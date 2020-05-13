# Use an official lightweight Python image.
# https://hub.docker.com/_/python
FROM python:3.8

WORKDIR /app

# Install production dependencies.
ADD requirements.txt /app/
RUN pip install -r requirements.txt

# Copy local code to the container image.

COPY ./app /app

# Service must listen to $PORT environment variable.
# This default value facilitates local development.
ENV PORT 80

# Run the web service on container startup. Here we use the gunicorn
# webserver, with one worker process and 8 threads.
# For environments with multiple CPU cores, increase the number of workers
# to be equal to the cores available.
CMD exec gunicorn --bind 0.0.0.0:$PORT --workers 1 --threads 1 --timeout 0 main:app
