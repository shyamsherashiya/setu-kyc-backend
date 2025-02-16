import requests
from app.core.config import settings
from typing import Dict, Any

class SetuAPIClient:
    def __init__(self):
        self.base_headers = {
            "x-client-id": settings.setu_client_id,
            "x-client-secret": settings.setu_client_secret,
            "x-product-instance-id": settings.setu_product_instance_id
        }

    async def verify_pan(self, pan: str) -> Dict[str, Any]:
        url = "https://dg-sandbox.setu.co/api/verify/pan"
        payload = {
            "pan": pan,
            "consent": "Y",
            "reason": "KYC verification as per regulatory requirements"
        }
        response = requests.post(
            url, 
            json=payload,
            headers={**self.base_headers, "Content-Type": "application/json"}
        )
        return self._handle_response(response)

    async def verify_bank_account(self, account_number: str, ifsc: str) -> Dict[str, Any]:
        url = "https://dg-sandbox.setu.co/api/verify/ban"
        payload = {
            "ifsc": ifsc,
            "accountNumber": account_number,
        }
        self.base_headers['x-product-instance-id'] = "9480d765-ebaf-4061-91d4-66af89c3e434"
        response = requests.post(
            url, 
            json=payload,
            headers={**self.base_headers, "Content-Type": "application/json"}
        )
        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        if response.status_code != 200:
            return {
                "status": "error",
                "code": response.status_code,
                "message": "API request failed",
                "details": response.text
            }
        return response.json()