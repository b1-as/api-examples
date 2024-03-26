import os

import requests
from dotenv import load_dotenv

load_dotenv()


HOST_NAME = os.getenv("BX_API_HOSTNAME")
JWT_TOKEN = os.getenv("BX_JWT")


session = requests.Session()


headers = {
    "Content-type": "application/json",
    "COOKIE": f"JWT_COOKIE={JWT_TOKEN}",
}

response = session.get(
    HOST_NAME + "/trading-api/v1/accounts/asset",
    headers=headers,
    verify=False,
)
print(f"GET {response.url}, HTTP Status: {response.status_code}, \n{response.text}")
