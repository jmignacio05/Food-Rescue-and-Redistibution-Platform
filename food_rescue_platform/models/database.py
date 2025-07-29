from pymongo import MongoClient

class Database:
    def __init__(self, uri="mongodb://localhost:27017/", db_name="food_rescue"):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]
        self.users = self.db["users"]
        self.food_items = self.db["food_items"]

    def add_user(self, user_dict):
        self.users.insert_one(user_dict)

    def find_user(self, user_id):
        return self.users.find_one({"user_id": user_id})

    def add_food_item(self, food_dict):
        self.food_items.insert_one(food_dict)

    def list_available_food(self):
        return list(self.food_items.find({"is_claimed": False}))

    def claim_food_item(self, item_id, recipient_id):
        return self.food_items.update_one(
            {"item_id": item_id, "is_claimed": False},
            {"$set": {"is_claimed": True, "recipient_id": recipient_id}}
        )

    def list_user_food(self, donor_id):
        return list(self.food_items.find({"donor_id": donor_id}))

    def list_claimed_food(self, recipient_id):
        return list(self.food_items.find({"recipient_id": recipient_id, "is_claimed": True}))
