import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

HOST_NAME = os.getenv("BX_API_HOSTNAME")
JWT_TOKEN = os.getenv("BX_JWT")
TRADING_ACCOUNT_ID = os.getenv("BX_TRADING_ACCOUNT_ID")
session = requests.Session()

headers = {
    "Content-type": "application/json",
    "Authorization": f"Bearer {JWT_TOKEN}",
}

response = session.get(
    HOST_NAME
    + "/trading-api/v1/history/borrow-interest"
    + f"?tradingAccountId={TRADING_ACCOUNT_ID}"
    + f"&assetSymbol=BTC"
    + f"&createdAtDatetime[gte]=2021-10-01T00:00:00.000Z"
    + f"&createdAtDatetime[lte]=2021-12-31T23:59:59.999Z"
    ,
    headers=headers,
    )
print("Raw response", response)
response_json = json.dumps(response.json(), indent=2)
print(f"HTTP Status: {response.status_code}, \n{response_json}")
