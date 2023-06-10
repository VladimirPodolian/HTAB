from random import randint

import pytest

from tests.conftest import xfail_mark


def test_add_user(ws, fake_data):
    """
    Adding a user with unique data
    """
    message = ws.add(**fake_data)
    ws.assert_success(message)


def test_add_duplicated_user_with_same_phone(ws, add_user, fake_data):
    """
    Check that it isn't possible to add user with same phone number
    """
    message = ws.add(**fake_data)
    ws.assert_failure(message)


def test_add_duplicated_user_with_different_phone(ws, add_user, fake_data):
    """
    Check that it is possible to add user with same phone number
    """
    message = ws.add(**fake_data)
    ws.assert_failure(message)


@pytest.mark.parametrize(
    'case',
    (
            pytest.param('name', marks=xfail_mark('User can be added with empy first name')),
            pytest.param('surname', marks=xfail_mark('User can be added with empy last name')),
            'phone',
            'age'
    )
)
def test_add_user_with_missed_info(ws, case, fake_data):
    fake_data.pop(case)
    message = ws.add(**fake_data)
    ws.assert_failure(message)


@pytest.mark.parametrize(
    'case',
    (
            'name',
            'surname',
            pytest.param('phone', marks=xfail_mark('Phone can be provided as integer, but should be string')),
            'request_id'
    )
)
def test_add_with_invalid_data(ws, fake_data, case):
    fake_data[case] = randint(10, 999)  # noqa
    message = ws.add(**fake_data)
    ws.assert_failure(message)

