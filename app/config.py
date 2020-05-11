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
import os

# ActiveMQ connection config
ACTIVEMQ_SERVER_HOSTNAME = os.getenv('ACTIVEMQ_SERVER_HOSTNAME')
ACTIVEMQ_SERVER_PORT = os.getenv('ACTIVEMQ_SERVER_PORT')
ACTIVEMQ_SERVER_USERNAME = os.getenv('ACTIVEMQ_SERVER_USERNAME')
ACTIVEMQ_SERVER_PASSWORD = os.getenv('ACTIVEMQ_SERVER_PASSWORD')

# Base url to where the messages must be proxied to
WEBHOOK_BASE_URL = os.getenv('WEBHOOK_BASE_URL', 'http://localhost:8883/api/plugins/reports/v1.0')
# Path appended to WEBHOOK_BASE_URL where messages will be proxied to
WEBHOOK_MESSAGE_PATH = os.getenv('WEBHOOK_MESSAGE_PATH', '/green-valley/message')
# Shared secret between this server and the server which receives the messages
WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET')
# Path appended to WEBHOOK_BASE_URL where topics will be fetched from
TOPICS_PATH = os.getenv('TOPICS_PATH', '/green-valley/topics')
