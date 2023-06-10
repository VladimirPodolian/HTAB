


def test_delete(ws):
    message = ws.delete(12345)
    print(f"Received: {message}")

def test_add(ws):
    message = ws.add(name='bob', surname='charlie', phone='12345', age=60)
    print(f"Received: {message}")
    message = ws.add(name='bob', surname='miles', phone='123456', age=20)
    print(f"Received: {message}")
