class User:
    def __init__(self, user_id, name, user_type, contact_info, password):
        self.user_id = user_id
        self.name = name
        self.user_type = user_type
        self.contact_info = contact_info
        self.password = password

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "name": self.name,
            "user_type": self.user_type,
            "contact_info": self.contact_info,
            "password": self.password
        }
