from websockets.sync.client import ClientConnection
import json


class Api:

    def __init__(self, ws:  ClientConnection):
        self.ws = ws

    def _send(self, payload: str):
        """
        A little logger added to default `send` command for better readability in test session

        :param payload: request payload in string format
        :return:
        """
        print(f'Send command with {payload=}')
        self.ws.send(payload)

    def _recv(self) -> dict:
        """
        Server responded with string format, and it's difficult to work with it
        Here is a wrapper under original `recv` method that format string into dict

        :return: dict object with response data
        """
        return json.loads(self.ws.recv())

    def delete(self, phone) -> dict:
        self.ws.send(json.dumps({"method": "delete", "id": "1", "phone": str(phone)}))
        return self._recv()

    def select(self, phone='', name='', surname=''):
        """
        Можно выбирать по телефону (он уникален, один юзер),
        либо по фамилии или имени (по отдельности, все юзеры которые совпадут).
        Запрос: - id: string, идентификатор запроса - met
        :return:
        """
        payload = {"method": "select", "id": "2"}

        if phone:
            payload.update({"phone": str(phone)})
        if name:
            payload.update({"name": name})
        if surname:
            payload.update({"surname": surname})

        self._send(json.dumps(payload))
        return self._recv()

    def select_by_name(self, name):
        return self.select(name=name)

    def select_by_surname(self, surname):
        return self.select(surname=surname)

    def add(self, name='', surname='', phone='', age=''):
        self._send(json.dumps(
            {
                "method": "add",
                "id": "3",
                "name": name,
                "surname": surname,
                "phone": str(phone),
                "age": age
            }
        ))
        return self._recv()

    @staticmethod
    def assert_success(response):
        assert response['status'] == 'success', f'The request is failed. Full response is: {response}'

    @staticmethod
    def is_failure(response):
        return response['status'] == 'failure', f'The request is succeed. Full response is: {response}'
