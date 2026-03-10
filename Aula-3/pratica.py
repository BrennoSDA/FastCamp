#Importando os principais pacotes para lidar com validadores
import enum
import hashlib
import re
from typing import Any

from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    field_validator,
    model_validator,
    SecretStr,
    ValidationError,
)

#definindo o que será válido e aceito em termos de caracteres
VALID_PASSWORD_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")
VALID_NAME_REGEX = re.compile(r"^[a-zA-Z]{2,}$")

#Adicionando CPF e Endereco(Adress)
VALID_CPF_REGEX = re.compile(r"^(?=.*\d).{8,})$")
VALID_ADRESS_REGEX = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$")

#Fazendo a classe user com os novos campos adicionados para validar dados
#CPF e Adress decidi deixar com frozen true para não poder ser mudado facilmente
class User(BaseModel):
    name: str = Field(examples=["Arjan"])
    email: EmailStr = Field(
        examples = ["user@arjancodes.com"],
        description ="The email of the user",
        frozen = True
    )
    password: SecretStr = Field(
        examples = ["Password123"], description = "The password of the user"
    )
    role: Role = Field(default = None, description = "The role of the user")
    cpf: CPF = Field(
        defalt = None, 
        description = "The CPF of the user",
        frozen = True
        )
    adress: Adress = Field(
        examples = ["Rua abc Qd. 01 Lt 01 - 00000-000"],
        description = "The adress of the user",
        frozen = True
    )