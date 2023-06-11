import pytest
from websockets.sync.client import connect

from src.api import Api
from src.utils import get_random_data


@pytest.fixture(scope='module')
def ws() -> Api:
    with connect("ws://127.0.0.1:4000") as websocket:
        api = Api(ws=websocket)
        yield api


@pytest.fixture(autouse=True)
def clear_user(ws, fake_data):
    yield
    ws.delete(phone=fake_data.get('phone'))


@pytest.fixture
def fake_data(ws):
    return get_random_data()


@pytest.fixture
def add_user(ws, fake_data):
    ws.add(**fake_data)
