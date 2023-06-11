import os
from random import randint

import pytest
from faker import Faker


def payload_builder(**kwargs):
    """
    Payload builder. Can be used with full locals

    :param kwargs: any keyword arguments ~
      name='Bob'
      surname=None
      phone='12346'
      self=object
    :return: dict object ~ {'name': 'Bob', 'phone': '12346'}
    """
    kwargs.pop('self', None)
    kwargs['id'] = str(os.getpid())

    payload = {}

    for key, value in kwargs.items():
        if value is not None:
            payload.update({key: value})

    return payload


def assert_success(response: dict) -> None:
    """
    Asserting that response status field is success

    :param response: dict object with response
    :return: None
    """
    assert response['status'] == 'success', f'The request is failed. Full response is: {response}'


def assert_failure(response: dict) -> None:
    """
    Asserting that response status field is failure

    :param response: dict object with response
    :return: None
    """
    assert response['status'] == 'failure', f'The request is succeed. Full response is: {response}'
    # Todo: too much errors for this
    # assert response.get('reason'), f'There are no reason field for error response: {response}'


def xfail_mark(reason):
    """
    Xfail mark with strict=True

    :param reason: xfail reason
    :return: xfail mark
    """
    return pytest.mark.xfail(reason=reason, strict=True)


def get_random_data() -> dict:
    """
    Get random user data

    :return: dict with required data
    """
    pid = str(os.getpid())
    fake = Faker()
    return dict(
        name=fake.first_name() + pid,
        surname=fake.last_name() + pid,
        phone=fake.basic_phone_number(),
        age=randint(0, 100),
    )
