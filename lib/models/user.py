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