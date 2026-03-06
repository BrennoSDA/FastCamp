from enum import auto, IntFlag
from typing import Any

from pydantic import(
    BaseModel,
    EmailStr,
    Field,
    SecretBytes,
    ValidationError,
)

class role(IntFlag):
    Author = auto()
    Editor = auto()
    Developer = auto()
    Admin = Author | Editor | Developer

class user(BaseModel):
    name: str = Field(examples = ["Arjan"])
    email: EmailStr = Field(
        examples = ["example@arjancodes.com"],
        description = "the email address of the user",
        frozen = True,
    )

        