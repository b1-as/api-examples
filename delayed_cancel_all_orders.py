import json
import os
from datetime import datetime, timezone
from hashlib import sha256
import requests
from eosio_signer import EOSIOKey
from dotenv import load_dotenv

load_dotenv()

HOST_NAME = os.getenv("BX_API_HOSTNAME")
PRIVATE_KEY = os.getenv("BX_PRIVATE_KEY")
JWT_TOKEN = os.getenv("BX_JWT")
AUTHORIZER = os.getenv("BX_AUTHORIZER")
TRADING_ACCOUNT_ID = os.getenv("BX_TRADING_ACCOUNT_ID")
DELAY_SEC = os.getenv("BX_DELAY_CANCEL_ALL_SECONDS")
lastNonce = os.getenv("BX_LAST_NONCE")

session = requests.Session()
response = session.get(HOST_NAME + "/trading-api/v1/nonce", verify=False)
nonceLowerBound = json.loads(response.text)["lowerBound"]
print(f"nonceLowerBound={nonceLowerBound}, lastNonce={lastNonce}")
if lastNonce is None:
    next_nonce = str(nonceLowerBound + 1)
else:
    next_nonce = str(int(lastNonce) + 1)
os.putenv("BX_LAST_NONCE", next_nonce)
timestamp = str(int(datetime.now(timezone.utc).timestamp() * 1000))

null = None
body = {
    "timestamp": timestamp,
    "nonce": next_nonce,
    "authorizer": AUTHORIZER,
    "command": {
        "commandType": "V1DelayedCancelAllOrders",
        "delayBySeconds": DELAY_SEC,
        "cancelId": "202308250900",
        "tradingAccountId": TRADING_ACCOUNT_ID
    }
}

print(f"Payload: {body}")

payload = (json.dumps(body, separators=(",", ":"))).encode("utf-8")
digest = sha256(payload.rstrip()).hexdigest()
eos_key = EOSIOKey(PRIVATE_KEY)
signature = eos_key.sign(digest)

headers = {
    "Content-type": "application/json",
    "Authorization": f"Bearer {JWT_TOKEN}",
    "BX-SIGNATURE": signature,
    "BX-TIMESTAMP": timestamp,
    "BX-NONCE": next_nonce,
}

response = session.post(
    HOST_NAME + "/trading-api/v1/command?commandType=V1DelayedCancelAllOrders", json=body, headers=headers
)
print(f"HTTP Status: {response.status_code}, \n{response.text}")
