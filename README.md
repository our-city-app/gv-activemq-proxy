# gv-activemq-proxy
Server which proxies messages received via ActiveMQ to an http(s) endpoint

## setup

### development

Create a docker-compose.yml file:

```yaml
version: '3'
services:
  gv-proxy:
    build: .
    volumes:
      - ./app:/app
    ports:
      - "80:80"
    container_name: gv-proxy
    restart: unless-stopped
    environment:
      - FLASK_APP=main.py
      - ACTIVEMQ_SERVER_HOSTNAME=activemq-teststomp.onlinesmartcities.be
      - ACTIVEMQ_SERVER_PORT=61613
      - ACTIVEMQ_SERVER_PASSWORD=activemq-password
      - ACTIVEMQ_SERVER_USERNAME=activemq-username
      - WEBHOOK_BASE_URL=http://some-host.domain.com/api/plugins/reports/v1.0
      - WEBHOOK_SECRET=webhook shared secret
      - FLASK_DEBUG=1
    command: python main.py --host=0.0.0.0 --port=80
```

Then start a development server:

- Download and install [docker](https://docs.docker.com/get-docker) and [docker-compose](https://docs.docker.com/compose/install)
- run `docker-compose up --build`

Alternatively, you can manually run the flask server as well (for debugging for example)

```shell script
FLASK_APP = app/main.py
FLASK_ENV = development
FLASK_DEBUG = 1
ACTIVEMQ_SERVER_HOSTNAME = ....
# ...plus the other env variables
python app/main.py
```

### Production:
- copy docker-compose.yml from development
- change the env variables to the production environment ones
- change FLASK_DEBUG to 0 
- remove the 'command' block.

This will use a uwsgi server to server requests instead of the development server.
