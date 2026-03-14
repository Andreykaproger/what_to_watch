from apiflask import Schema
from apiflask.fields import String, Integer, Email, Boolean, List, Nested, DateTime
from marshmallow import validates, ValidationError


class UserOutputSchema(Schema):
    id = Integer()
    Email = Email()
    username = String()
    is_active = Boolean()
    role = String()

class UsersListSchema(Schema):
    number_of_users = Integer()

    users = List(Nested(UserOutputSchema))

class BlockUserSchema(Schema):
    reason = String(required=True)

    @validates("reason")
    def validate_reason(self, value, **kwargs):
        if not value.strip():
            raise ValidationError("Укажите причину блокировки")

class OpinionsOutputSchema(Schema):
    id = Integer()
    title = String()
    text = String()
    source = String()
    timestamp = DateTime()
    user_id = Integer()
    status = String()

class OpinionsListSchema(Schema):
    number_of_opinions = Integer()

    opinions = List(Nested(OpinionsOutputSchema))
