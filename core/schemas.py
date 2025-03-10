from pydantic import BaseModel


class AddPasswordSchema(BaseModel):
    password: str


class PasswordSchema(AddPasswordSchema):
    service_name: str


