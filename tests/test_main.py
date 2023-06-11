import os

import pytest

from src.utils import assert_failure


@pytest.mark.parametrize('case', ('name', 'surname', 'phone', 'age', 'method', 'id'))
@pytest.mark.parametrize('method', ('select', 'update', 'abracadabra', 123, None))
@pytest.mark.parametrize(
    'injection',
    (
            'user"});alert(document.cookie);({"accountType":"user',
            'javascript:alert(‘Executed!’);'
            'DROP TABLE USERS;'
    )
)
def test_request_injection(ws, fake_data, case, method, injection):
    fake_data.update({case: injection, 'method': method, 'id': str(os.getpid())})
    message = ws.send(fake_data).recv()
    assert_failure(message)
