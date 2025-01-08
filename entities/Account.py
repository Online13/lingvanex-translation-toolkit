from pydantic import BaseModel

class Account(BaseModel):
    email: str | None
    token: str
    expired: bool = False