from __future__ import annotations

from websockets.sync.client import ClientConnection
import json

from src.utils import payload_builder


class Api:

    def __init__(self, ws: ClientConnection):
        self.ws: ClientConnection = ws

    def add(self, name=None, surname=None, phone=None, age=None):
        return self.request('add', locals())

    def select(self, phone=None, name=None, surname=None, age=None):
        return self.request('select', locals())

    def update(self, name=None, surname=None, phone=None, age=None):
        return self.request('update', locals())

    def delete(self, name=None, surname=None, phone=None, age=None):
        return self.request('delete', locals())

    def request(self, method: str, data: dict) -> dict:
        """
        Default request builder

        :param method: command method to be sent
        :param data: payload data
        :return: response dict
        """
        payload = {
            "method": method,
            **payload_builder(**data)
        }

        response = self.send(payload).recv()

        assert response['id'] == payload['id'],\
            'Unexpected id in response.\nPayload: {payload}\nResponse: {response}'

        return response

    def send(self, payload: dict) -> Api:
        """
        A little logger added to default `send` command for better readability in test session

        :param payload: request payload
        :return: self
        """
        print(f'Send command with {payload=}')
        self.ws.send(json.dumps(payload))
        return self

    def recv(self) -> dict:
        """
        Server responded with string format, and it's difficult to work with it
        This is a wrapper under original `recv` method that format string into dict

        :return: dict object with response data
        """
        return json.loads(self.ws.recv())
