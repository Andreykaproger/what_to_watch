from apiflask import Schema
from apiflask.fields import String, Email, Integer

from . import MessageOutputSchema

class RegisterSchema(Schema):
    username = String(required=True)
    email = Email(required=True)
    password = String(required=True)


class LoginSchema(Schema):
    email = Email(required=True)
    password = String(required=True)

class ProfileSchema(Schema):
    id = Integer()
    email = Email()
    username = String()

class RefreshTokenSchema(Schema):
    access_token = String()

class TokenSchema(MessageOutputSchema, RefreshTokenSchema):
    access_token = String()
    refresh_token = String()

