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

import aiohttp

from config import WEBHOOK_BASE_URL, WEBHOOK_MESSAGE_PATH, TOPICS_PATH, WEBHOOK_SECRET


async def get_topics():
    async with aiohttp.ClientSession() as session:
        async with session.request('GET', WEBHOOK_BASE_URL + TOPICS_PATH) as response:
            response.raise_for_status()
            return await response.json()


def send_request(integration_id: int, data: str):
    try:
        asyncio.run(_send_request(integration_id, data))
    except Exception:
        logging.exception('Could not send request')
        # TODO retry


async def _send_request(integration_id: int, data: str):
    async with aiohttp.ClientSession() as session:
        url = f'{WEBHOOK_BASE_URL}{WEBHOOK_MESSAGE_PATH}/{integration_id}'
        headers = {'Authorization': WEBHOOK_SECRET}
        async with session.request('POST', url, data=data, headers=headers) as response:
            response.raise_for_status()
