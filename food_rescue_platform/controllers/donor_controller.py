from models.food_item import FoodItem

class DonorController:
    def __init__(self, db):
        self.db = db

    def post_food(self, donor_id, name, quantity, expiry_date, location):
        food_item = FoodItem(
            item_id=self.db.food_items.count_documents({}) + 1,
            name=name,
            quantity=quantity,
            expiry_date=expiry_date,
            donor_id=donor_id,
            location=location
        )
        self.db.add_food_item(food_item.to_dict())

    def view_my_food(self, donor_id):
        return self.db.list_user_food(donor_id)
