from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    id: int = None
    username: str = None
    email: str = None
    password_hash: str = None
    first_name: str = None
    last_name: str = None
    created_at: datetime = None
    updated_at: datetime = None
        
    def __str__(self):
        return f"User({self.id}, {self.username}, {self.email}, {self.first_name}, {self.last_name})"

    # These next two methods will be used by the controller to check if
    # books are valid and if not show errors to the user.
    def is_valid(self):
        if self.username == None or self.username == "":
            return False
        if self.email == None or self.email == "":
            return False
        if self.password_hash == None or self.password_hash == "":
            return False
        if self.first_name == None or self.first_name == "":
            return False
        if self.last_name == None or self.last_name == "":
            return False
        return True

    def generate_errors(self):
        errors = []
        if self.username == None or self.username == "":
            errors.append("Username can't be blank")
        if self.email == None or self.email == "":
            errors.append("Email can't be blank")
        if self.password_hash == None or self.password_hash == "":
            errors.append("Password_hash can't be blank")
        if self.first_name == None or self.first_name == "":
            errors.append("First name can't be blank")
        if self.last_name == None or self.last_name == "":
            errors.append("Last name can't be blank")
        if len(errors) == 0:
            return None
        else:
            return ", ".join(errors)


    # def to_dict(self):
    #     return {
    #         'id': self.id,
    #         'username': self.username,
    #         'email': self.email,
    #         # 'password_hash': self.password_hash, # Usually don't expose this!
    #         'first_name': self.first_name,
    #         'last_name': self.last_name,
    #         'created_at': self.created_at.isoformat() if self.created_at else None,
    #         'updated_at': self.updated_at.isoformat() if self.updated_at else None
    #     }