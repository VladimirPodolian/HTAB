import pytest

from src.utils import assert_success, assert_failure


def test_update_user(ws, add_user, fake_data):
    """
    Update user with full info
    """
    message = ws.update(**fake_data)
    assert_success(message)


@pytest.mark.parametrize(
    ('case', 'value'),
    (
        ('name', 'some_data'),
        ('surname', 'some_data'),
        ('phone', 'some_data'),
        ('age',  9999),
    ),
)
def test_update_with_incorrect_info(ws, add_user, fake_data, case, value):
    """
    User should not be flushed with incorrect info
    """
    if case in ('name', 'surname', 'age'):
        pytest.xfail(f'User is flushed even the `{case}` field is different')
    fake_data[case] = value
    message = ws.update(**fake_data)
    assert_failure(message)


def test_update_unavailable_user(ws, fake_data):
    """
    Server should raise an error for unavailable user
    """
    message = ws.update(**fake_data)
    assert_failure(message)


@pytest.mark.parametrize(
    ('case', 'value'),
    (
        ('name', ''),
        ('surname', ''),
        ('phone', ''),
        ('age',  0),
    ),
)
def test_update_with_invalid_data(ws, fake_data, case, value):
    """
    The server should respond with an error with reason for incorrect payload
    """
    fake_data[case] = value
    message = ws.update(**fake_data)
    assert_failure(message)
