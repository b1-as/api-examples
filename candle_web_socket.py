import json
import os
import threading
import time
from collections import deque
import websocket
from dotenv import load_dotenv

load_dotenv()

WS_HOST_NAME = os.getenv("BX_WS_API_HOSTNAME")

def get_id():
    return str(int(time.time() * 1000))


def ping(conn):
    ping_message = {
        "jsonrpc": "2.0",
        "type": "command",
        "method": "keepalivePing",
        "params": {},
        "id": get_id()
    }
    conn.send(json.dumps(ping_message))
    threading.Timer(interval=5, function=ping, args=(conn,)).start()


def on_message(conn, message):
    global TRADES, CURR_TRADE_ID
    message = json.loads(message)
    if "type" not in message:
        return
    print(message)


def on_error(conn, message):
    print(f"Received error: {message}")


def on_close(conn, close_status_code, close_msg):
    print(f"Closed connection to {conn.url}. close_status_code={close_status_code}, close_msg={close_msg}")


def open_connection():
    ws_conn = websocket.WebSocketApp(WS_HOST_NAME + "/v1/markets/BTCUSDC/candle",
                                     on_message=on_message,
                                     on_error=on_error,
                                     on_close=on_close)
    threading.Timer(interval=5, function=ping, args=(ws_conn,)).start()
    ws_conn.run_forever()


wst = threading.Thread(target=open_connection)
wst.start()
