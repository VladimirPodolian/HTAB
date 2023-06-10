from __future__ import annotations

from websockets.sync.client import ClientConnection
import json


class Api:

    def __init__(self, ws:  ClientConnection):
        self.ws = ws

    def select(self, phone=None, name=None, surname=None, age=None, request_id='2'):
        payload = {
            "method": "select",
            **self._payload_builder(phone=phone, name=name, surname=surname, age=age, id=request_id)
        }

        return self._send(payload)._recv()

    def add(self, name=None, surname=None, phone=None, age=None, request_id='1'):
        payload = {
            "method": "add",
            **self._payload_builder(phone=phone, name=name, surname=surname, age=age, id=request_id)
        }

        return self._send(payload)._recv()

    def delete(self, name=None, surname=None, phone=None, age=None, request_id='3'):
        payload = {
            "method": "delete",
            **self._payload_builder(phone=phone, name=name, surname=surname, age=age, id=request_id)
        }

        return self._send(payload)._recv()

    @staticmethod
    def assert_success(response):
        assert response['status'] == 'success', f'The request is failed. Full response is: {response}'

    @staticmethod
    def assert_failure(response):
        assert response['status'] == 'failure', f'The request is succeed. Full response is: {response}'

    @staticmethod
    def _payload_builder(**kwargs):
        payload = {}

        for key, value in kwargs.items():
            if value is not None:
                payload.update({key: value})

        return payload

    def _send(self, payload: dict) -> Api:
        """
        A little logger added to default `send` command for better readability in test session

        :param payload: request payload in dict format
        :return: self
        """
        print(f'Send command with {payload=}')
        self.ws.send(json.dumps(payload))
        return self

    def _recv(self) -> dict:
        """
        Server responded with string format, and it's difficult to work with it
        Here is a wrapper under original `recv` method that format string into dict

        :return: dict object with response data
        """
        return json.loads(self.ws.recv())
