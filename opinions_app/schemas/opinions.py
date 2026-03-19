from apiflask import Schema
from apiflask.fields import String, List, Nested, Integer
from marshmallow import validates, ValidationError



class UserOpinionSchema(Schema):

    id = Integer()

    user_id = Integer()

    title = String(required=True)

    text = String(required=True)

    source = String()

    @validates("title", "text")
    def validate_title(self, value, **kwargs):

        if not value.strip():
            raise ValidationError("Обязательное поле")


class UserOpinionsListSchema(Schema):
    opinions = List(Nested(UserOpinionSchema))

class BlockOpinionSchema(Schema):
    reason = String(required=True)

    @validates("reason")
    def validate_reason(self, value, **kwargs):

        if not value.strip():
            raise ValidationError("Укажите причину блокировки")


