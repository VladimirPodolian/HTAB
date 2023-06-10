import os

import pytest

from tests.conftest import get_random_data


@pytest.mark.xfail(reason='User is available, but status is failure', strict=True)
def test_select_by_phone_status(ws, add_user, fake_data):
    """
    Check response status after send `select` command with phone number
    """
    # TODO: should be merged with test_select_by_phone_user after bug fix from Joe
    message = ws.select(fake_data['phone'])
    ws.assert_success(message)


def test_select_by_phone_user(ws, add_user, fake_data):
    """
    Check user data after send `select` command with phone number
    """
    message = ws.select(phone=fake_data['phone'])
    assert message['users'][0] == fake_data


@pytest.mark.xfail(reason='User is available, but status is failure', strict=True)
def test_select_by_name_status(ws, add_user, fake_data):
    """
    Check response status after send `select` command with user first name
    """
    # TODO: should be merged with test_select_by_name after bug fix from Joe
    message = ws.select(name=fake_data['name'])
    ws.assert_success(message)


def test_select_by_name_users(ws, add_user, fake_data):
    """
    Check user data after send `select` command with user first name
    """
    message = ws.select(name=fake_data['name'])
    assert message['users'][0] == fake_data


@pytest.mark.xfail(reason='User is available, but status is failure', strict=True)
def test_select_by_surname_status(ws, add_user, fake_data):
    """
    Check response status after send `select` command with user last name
    """
    # TODO: should be merged with test_select_by_surname_users after bug fix from Joe
    message = ws.select(surname=fake_data['surname'])
    ws.assert_success(message)


def test_select_by_surname_users(ws, add_user, fake_data):
    """
    Check user data after send `select` command with user last name
    """
    message = ws.select(surname=fake_data['surname'])
    assert message['users'][0] == fake_data


@pytest.mark.parametrize('by', [
    'name',
    pytest.param(
        'surname',
        marks=pytest.mark.xfail(
            reason='Only one user received while selecting with user last name', strict=True
        )),
])
def test_select_multiple_users(ws, by, fake_data):
    """
    Check that multiple users can be received by `send` command
    """
    users_count = 5
    changeable_data = fake_data.copy()
    access_method = ws.select_by_name if by == 'name' else ws.select_by_surname

    for i in range(users_count):
        changeable_data['phone'] = fake_data['phone'] + str(i)  # should be unique
        ws.assert_success(ws.add(**changeable_data))

    users = access_method(fake_data[by])['users']  # noqa
    assert len(users) == users_count, f'Should be created {users_count} users, but {len(users)} received'
    changeable_data = fake_data.copy()

    for i in range(users_count):
        changeable_data['phone'] = fake_data['phone'] + str(i)
        assert users[i] == changeable_data

# todo select without adding users
