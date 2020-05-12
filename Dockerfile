FROM tiangolo/uwsgi-nginx-flask:python3.8

ADD requirements.txt /app/
RUN pip install -r requirements.txt

COPY ./app /app
