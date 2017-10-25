import websocket
import json
import sys

def parse_args():
    global lights
    if len(sys.argv) != 2:
      print_usage()
    if sys.argv[1] == 'mac':
      import lightstemp as lights
    elif sys.argv[1] == 'pi':
      import lights
    else:
      print_usage()
    return

def on_message(ws, message):
    # print(message)
    command = eval(message)
    # print(command)
    if command['type'] == 'light':
      if command['query'] == 'status':
        status = lights.get_status()
        reply = json.dumps(status)
      else:
        light_no = command['light']
        control = command['status']
        response = lights.control(light_no,control)
        reply = json.dumps(response)
    ws.send(reply)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print("### OPEN ###")

def print_usage():
    print("USAGE: python3 ws.py [mac/pi]")
    sys.exit(0)
    return


def main():
    parse_args()
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8000/connect",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    # print [method_name for method_name in dir(object)]# if callable(getattr(object, method_name))]
    ws.run_forever()


if __name__ == '__main__':
  main()