FROM tiangolo/uwsgi-nginx-flask:python3.8

COPY ./app /app

ADD requirements.txt /app/
RUN pip install -r requirements.txt
