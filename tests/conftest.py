import os
from random import randint

import pytest
from faker import Faker
from websockets.sync.client import connect

from src.api import Api


# todo broken request method


@pytest.fixture(scope='module')
def ws() -> Api:
    with connect("ws://127.0.0.1:4001") as websocket:
        api = Api(ws=websocket)
        yield api


def get_random_data():
    pid = str(os.getpid())
    fake = Faker()
    return dict(
        name=fake.first_name() + pid,
        surname=fake.last_name() + pid,
        phone=fake.basic_phone_number(),
        age=randint(0, 100)
    )


@pytest.fixture(autouse=True)
def clear_user(ws, fake_data):
    yield
    ws.delete(fake_data.get('phone'))


@pytest.fixture
def fake_data(ws):
    return get_random_data()


@pytest.fixture
def add_user(ws, fake_data):
    ws.add(**fake_data)


def xfail_mark(reason):
    return pytest.mark.xfail(reason=reason, strict=True)
