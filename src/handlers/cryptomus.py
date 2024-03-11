import json
import hashlib
import base64
from typing import Any
from aiohttp import ClientSession
from src.config.cfg import API_CRYPT, MERCHANT_UID

def generate_headers(data: str) -> dict[str, Any]:
    sign = hashlib.md5(
        base64.b64encode(data.encode('ascii')) + API_CRYPT.encode('ascii')
    ).hexdigest()

async def create_invoice(user_id: int, amount) -> Any:
    async with ClientSession() as session:
        json_dumps = json.dumps({
            "amount": str(amount),
            "order_id": f"MY-TEST-ORDER-{user_id}-000",
            "currency": "USDT",
            "network" : "tron",
            "Lifetime": 300
        })
        response = await session.post("https://api.cryptomus.com/v1/payment",
                                      data = json_dumps,
                                      headers=generate_headers(json_dumps)
        )
        return await response.json()

async def get_invoice(uuid: str) -> Any:
    async with ClientSession() as session: 
        json_dumps = json.dumps({"uuid": uuid})
        response = await session.post(
            "https://api.cryptomus.com/v1/payment/info",
            data = json_dumps, 
            headers = generate_headers(json_dumps)
        )
        return await response.json()