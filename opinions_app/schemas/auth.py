from apiflask import Schema
from apiflask.fields import String, Email, Integer
from marshmallow import validates, ValidationError

from . import MessageOutputSchema


class RegisterSchema(Schema):

    username = String(required=True)
    email = Email(required=True)
    password = String(required=True)

    @validates("username", "email", "password")
    def validate_fields(self, value, **kwargs):

        if not value.strip():
            raise ValidationError("Обязательное поле")



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

