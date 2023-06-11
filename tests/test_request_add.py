import os
from random import randint

import pytest

from src.utils import assert_failure, assert_success


def test_add_user(ws, fake_data):
    """
    Adding a user with unique data
    """
    message = ws.add(**fake_data)
    assert_success(message)


@pytest.mark.xfail(reason='It is possible to add user with negative age', strict=True)
def test_add_user_negative_age(ws, fake_data):
    """
    Adding a user with negative age
    """
    fake_data['age'] = -12
    message = ws.add(**fake_data)
    assert_failure(message)


def test_add_duplicated_user_with_same_phone(ws, add_user, fake_data):
    """
    Check that it isn't possible to add user with same phone number
    """
    message = ws.add(**fake_data)
    assert_failure(message)


def test_add_duplicated_user_with_different_phone(ws, add_user, fake_data):
    """
    Check that it is possible to add record with same data except phone number
    """
    fake_data['phone'] = str(os.getpid())
    message = ws.add(**fake_data)
    assert_success(message)


@pytest.mark.xfail(reason='User can be created with empty info', strict=True)
@pytest.mark.parametrize(
    ('case', 'value'),
    (
        ('name', ''),
        ('surname', ''),
        ('phone', ''),
        ('age',  0),
    ),
)
def test_add_user_with_empty_info(ws, case, fake_data, value):
    """
    Users with empty information should not be created
    """
    fake_data.update({case: value})
    message = ws.add(**fake_data)
    assert_failure(message)


@pytest.mark.parametrize(
    'case',
    (
            'name',
            'surname',
            'phone',
            'age'
    )
)
def test_add_user_with_missed_info(ws, case, fake_data):
    """
    User should not be created if some of required fields is missed in request payload
    """
    fake_data.pop(case)
    message = ws.add(**fake_data)
    assert_failure(message)
    assert f"key '{case}' not found" in message['reason']


@pytest.mark.parametrize(
    ('case', 'value'),
    (
        ('name', randint(10, 999)),
        ('surname', randint(10, 999)),
        ('phone', randint(10, 999)),
        ('age',  'data'),
    ),
)
def test_add_with_invalid_data(ws, fake_data, case, value):
    """
    All fields should be in string format except `age`, that should be an integer
    """
    error = 'type must be number' if case == 'age' else ' type must be string'
    fake_data[case] = value

    message = ws.add(**fake_data)
    assert_failure(message)
    assert error in message['reason']
