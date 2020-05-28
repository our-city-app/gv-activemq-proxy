# -*- coding: utf-8 -*-
# Copyright 2020 Green Valley NV
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# @@license_version:1.5@@
import logging
import threading
import time
from queue import Queue

import stomp
from flask import Flask, request, Response

from config import WEBHOOK_SECRET, ACTIVEMQ_SERVER_USERNAME, ACTIVEMQ_SERVER_PASSWORD, ACTIVEMQ_SERVER_HOSTNAME, \
    ACTIVEMQ_SERVER_PORT
from listener import GVListener, unsubscribe, subscribe

root = logging.getLogger()
root.name = 'gv-activemq-proxy'
root.setLevel(logging.DEBUG)

app = Flask(__name__)

q = Queue()


@app.route('/')
def index():
    url = 'https://github.com/our-city-app/gv-activemq-proxy'
    return f'Green valley ActiveMQ proxy<br>Source: <a href="{url}">{url}</a>'


def _validate_request() -> bool:
    auth = request.headers.get('Authorization')
    if auth != WEBHOOK_SECRET:
        logging.info('Invalid authorization %s', auth)
        return False
    return True


@app.route('/topics', methods=['POST'])
def on_topic_changed():
    if not _validate_request():
        return Response(status=401)
    integration_id = request.json.get('integration_id')
    topic = request.json.get('topic')
    command = request.json.get('command')
    if not topic or not command:
        return Response('Invalid request, expected \'topic\' and \'command\' in body', status=400)
    q.put([command, integration_id, topic])
    return Response(status=204)


def setup_connection(q: Queue):
    logging.info('Starting stomp connection on thread: %s', threading.current_thread())
    our_heartbeat_rate = 60000  # our server sends heartbeat every 60 seconds
    their_heartbeat_rate = 0  # their server does nothing
    conn = stomp.StompConnection12(host_and_ports=[(ACTIVEMQ_SERVER_HOSTNAME, int(ACTIVEMQ_SERVER_PORT))],
                                   keepalive=True, heartbeats=(our_heartbeat_rate, their_heartbeat_rate))
    conn.set_listener('listener name', GVListener(conn))
    conn.connect(ACTIVEMQ_SERVER_USERNAME, ACTIVEMQ_SERVER_PASSWORD, wait=True)
    while True:
        # Infinite loop - execute commands as they arrive from the server
        time.sleep(1)
        item = q.get()
        if item:
            command, integration_id, topic = item
            if command == 'subscribe':
                subscribe(conn, integration_id, topic)
            elif command == 'unsubscribe':
                unsubscribe(conn, integration_id, topic)


with app.app_context():
    thread = threading.Thread(target=setup_connection, args=[q])
    thread.start()

if __name__ == '__main__':
    # use_reloader=False is needed otherwise the connection above will be setup twice, for some reason.
    app.run(host='0.0.0.0', debug=True, port=80, use_reloader=False)
