class FoodItem:
    def __init__(self, item_id, name, quantity, expiry_date, donor_id, location, is_claimed=False, recipient_id=None):
        self.item_id = item_id
        self.name = name
        self.quantity = quantity
        self.expiry_date = expiry_date
        self.donor_id = donor_id
        self.location = location
        self.is_claimed = is_claimed
        self.recipient_id = recipient_id

    def to_dict(self):
        return {
            "item_id": self.item_id,
            "name": self.name,
            "quantity": self.quantity,
            "expiry_date": self.expiry_date,
            "donor_id": self.donor_id,
            "location": self.location,
            "is_claimed": self.is_claimed,
            "recipient_id": self.recipient_id
        }
