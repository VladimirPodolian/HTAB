


def test_delete(ws):
    message = ws.delete(12345)
    print(f"Received: {message}")


