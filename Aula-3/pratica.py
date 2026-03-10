#Ficou claro que o pydantic é muito útil para validar e serializar dados, por isso foi escolhido dois campos para fazer a demosntracão de conhecimento 
import enum
import hashlib
import re
from typing import Any, Self

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
    field_serializer,
    model_serializer,
    SecretStr,
)

#definindo a validade dos dados, o que é necessário ter e quantos caracteres são necessários
VALID_PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")  #letra maiuscula, minuscula e número, 8 caracteres (exemplo)
VALID_NAME_REGEX = re.compile(r"^[a-zA-Z]{2,}$")
VALID_CPF_REGEX = re.compile(r"^\d{11}$")
VALID_ADDRESS_REGEX = re.compile(r"^.{7,}$")

#Apenas dois tipos de usuário para facilitar
class Role(enum.IntEnum):
    User = 1
    Admin = 2

#definindo quais campos o usuário terá, ou seja, quais serão seus dados
class User(BaseModel):
    name: str = Field(examples=["Arjan"])

    email: EmailStr = Field(
        examples=["user@arjancodes.com"],
        description="The email address of the user",
        frozen=True,
    )

    password: SecretStr = Field(
        examples=["Password123"],
        description="The password of the user",
        exclude=True,
    )

    role: Role = Field(
        description="The role of the user",
        default=Role.User,
        validate_default=True,
    )

    cpf: str = Field(
        description="The CPF of the user",
        frozen=True
    )

    address: str = Field(
        examples=["Rua abc Qd. 01 Lt 01 - 00000-000"],
        description="The address of the user",
        frozen=True
    )

#Validacão do campo nome, ele irá rodar quando o campo nome for lido
    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        if not VALID_NAME_REGEX.match(v):
            raise ValueError(
                "Name is invalid, must contain only letters and be at least 2 characters long"
            )
        return v

#Validacão do campo CPF, ele irá rodar quando o campo CPF for lido
    @field_validator("cpf")
    @classmethod
    def validate_cpf(cls, v: str) -> str:
        if not VALID_CPF_REGEX.match(v):
            raise ValueError(
                "CPF is invalid, must contain exactly 11 numbers"
            )
        return v

#Validacão do campo endereco, ele irá rodar quando o campo adress for lido
    @field_validator("address")
    @classmethod
    def validate_address(cls, v: str) -> str:
        if not VALID_ADDRESS_REGEX.match(v):
            raise ValueError(
                "Address is invalid, must contain at least 5 characters"
            )
        return v

    @field_validator("role", mode="before")
    @classmethod
    def validate_role(cls, v: int | str | Role) -> Role:
        op = {int: lambda x: Role(x), str: lambda x: Role[x], Role: lambda x: x}
        try:
            return op[type(v)](v)
        except (KeyError, ValueError):
            raise ValueError(
                f"Role is invalid, please use one of the following: {', '.join([x.name for x in Role])}"
            )

#Validacao de todos os campos juntos, verifica se senha tem o nome também, valida a senha e criptografa
    @model_validator(mode="before")
    @classmethod
    def validate_user_pre(cls, v: dict[str, Any]) -> dict[str, Any]:

        required_fields = ["name", "password", "cpf", "address"]

        for field in required_fields:
            if field not in v:
                raise ValueError(f"{field} is required")

        password = v["password"]

        if v["name"].casefold() in password.casefold():
            raise ValueError("Password cannot contain name")

        if not VALID_PASSWORD_REGEX.match(password):
            raise ValueError(
                "Password is invalid, must contain 8 characters, 1 uppercase, 1 lowercase, 1 number"
            )

#Criptografia
        v["password"] = hashlib.sha256(password.encode()).hexdigest()

        return v

#Apenas o Arjan será admin, como se fosse um sistema real
    @model_validator(mode="after")
    def validate_user_post(self) -> Self:
        if self.role == Role.Admin and self.name != "Arjan":
            raise ValueError("Only Arjan can be an admin")
        return self

#Serializacao pós leitura para colocar os dados em formato json para serem lidos pela API
    @field_serializer("role", when_used="json")
    @classmethod
    def serialize_role(cls, v) -> str:
        return v.name

    @model_serializer(mode="wrap", when_used="json")
    def serialize_user(self, serializer, info) -> dict[str, Any]:
        if not info.include and not info.exclude:
            return {
                "name": self.name,
                "role": self.role.name,
                "cpf": self.cpf,
                "address": self.address,
            }
        return serializer(self)