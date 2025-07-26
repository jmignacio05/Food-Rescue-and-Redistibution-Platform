
import requests

API_URL = "http://127.0.0.1:8000"

class RecipientController:
    def __init__(self, db=None):
        self.db = db  # Kept for compatibility, not used with API

    def list_available_food(self):
        resp = requests.get(f"{API_URL}/food")
        resp.raise_for_status()
        # Only return unclaimed food
        return [item for item in resp.json() if not item.get("is_claimed")]

    def list_claimed_food(self, recipient_id):
        resp = requests.get(f"{API_URL}/food")
        resp.raise_for_status()
        # Ensure type consistency for recipient_id
        def id_match(item_id):
            return str(item_id) == str(recipient_id)
        return [item for item in resp.json() if item.get("is_claimed") and id_match(item.get("recipient_id"))]

    def claim_food(self, food_item_id, recipient_id):
        data = {"item_id": food_item_id, "recipient_id": recipient_id}
        resp = requests.post(f"{API_URL}/claim", json=data)
        resp.raise_for_status()
        return resp.json()
