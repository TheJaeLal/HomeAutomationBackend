from websocket import enableTrace, WebSocketApp

def on_message(ws, message):
    print(message)
    ws.send(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### OPEN ###")


if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000/connect",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    # print [method_name for method_name in dir(object)]# if callable(getattr(object, method_name))]
    ws.run_forever()