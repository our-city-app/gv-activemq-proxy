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
import asyncio
import logging
import sys

from aiohttp import ClientResponseError
from stomp import ConnectionListener, StompConnection12

from webhooks import send_request, get_topics

SUB_ID = 'subscription-%s'


def subscribe(connection: StompConnection12, topic: str):
    logging.info(f'Subscribing to {topic}')
    connection.subscribe(topic, SUB_ID % topic)


def unsubscribe(connection: StompConnection12, topic: str):
    logging.info(f'Unsubscribing to {topic}')
    connection.unsubscribe(SUB_ID % topic)


async def setup_subscriptions(connection: StompConnection12):
    logging.debug('Setting up subscriptions')
    try:
        for topic in await get_topics():
            subscribe(connection, topic)
    except ClientResponseError:
        logging.exception('Could not fetch topics')
        sys.exit(1)


class GVListener(ConnectionListener):

    def __init__(self, connection: StompConnection12):
        self.connection = connection

    def on_connecting(self, host_and_port):
        """
        Called by the STOMP connection once a TCP/IP connection to the
        STOMP server has been established or re-established. Note that
        at this point, no connection has been established on the STOMP
        protocol level. For this, you need to invoke the "connect"
        method on the connection.

        :param (str,int) host_and_port: a tuple containing the host name and port number to which the connection
            has been established.
        """
        logging.info('Connecting to %s', host_and_port)

    def on_connected(self, headers, body):
        """
        Called by the STOMP connection when a CONNECTED frame is
        received (after a connection has been established or
        re-established).

        :param dict headers: a dictionary containing all headers sent by the server as key/value pairs.
        :param body: the frame's payload. This is usually empty for CONNECTED frames.
        """
        logging.info('Connected!')
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(setup_subscriptions(self.connection))

    def on_disconnected(self):
        """
        Called by the STOMP connection when a TCP/IP connection to the
        STOMP server has been lost.  No messages should be sent via
        the connection until it has been reestablished.
        """
        logging.info('Disconnected!')

    def on_message(self, headers, body):
        """
        Called by the STOMP connection when a MESSAGE frame is received.

        :param dict headers: a dictionary containing all headers sent by the server as key/value pairs.
        :param body: the frame's payload - the message body.
        """
        logging.info('Received message %s', body)
        send_request(body)

    def on_error(self, headers, body):
        """
        Called by the STOMP connection when an ERROR frame is received.

        :param dict headers: a dictionary containing all headers sent by the server as key/value pairs.
        :param body: the frame's payload - usually a detailed error description.
        """
        logging.error('Error: %s', body)
