from random import randint

import pytest

from src.utils import assert_failure, assert_success


def test_delete_user_by_phone_number(ws, add_user, fake_data):
    """
    Deleting a user by phone number
    """
    delete_response = ws.delete(phone=fake_data['phone'])
    assert_success(delete_response)
    select_response = ws.select(surname=fake_data['surname'])
    assert not select_response.get('users')


def test_delete_user_by_unavailable_phone_number(ws, fake_data):
    """
    The server should return an error with reason field
      for `delete` command with unavailable phone
    """
    delete_response = ws.delete(phone=fake_data['phone'])
    assert_failure(delete_response)


@pytest.mark.parametrize(
    'case',
    (
            'name',
            'surname',
            'age',
    )
)
def test_delete_by_other_data(ws, add_user, fake_data, case):
    """
    User should not be deleted by other data
    """
    delete_response = ws.delete(**{case: fake_data[case]})
    assert_failure(delete_response)
    assert "key 'phone' not found" in delete_response['reason']
    select_response = ws.select(surname=fake_data['surname'])
    assert select_response['users'][0] == fake_data


def test_delete_with_invalid_data(ws, fake_data):
    """
    Send a `delete` command with `phone` field in integer format
    """
    message = ws.delete(phone=randint(10, 999))
    assert_failure(message)
    assert 'type must be string, but is number' in message['reason']
