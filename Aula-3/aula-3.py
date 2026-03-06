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
    password: SecretStr = Field(
        examples = ["Password123"], description = "The password of the user"
    )
    role: Role = Field(default = None, description = "The role of the user")

def validate (data: dict[str, Any]) -> None:
    try:
        user = User.model_validate(data)
        print(user)
    except ValidationError as e:
        print("User is invalid")
        for error in e.erros():
            print(error)

def main() -> None:
    good_data = {
        "name": "Arjan", 
        "email": "example@arjancodes.com",
        "password": "Password123"
        }

    bad_data = {"email": "<bad data>", "password": "<bad data>"}

    validate(good_data)
    validate(bad_data)