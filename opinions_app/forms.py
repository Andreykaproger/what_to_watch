from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SubmitField
from wtforms.validators import DataRequired, Length, Optional

class OpinionForm(FlaskForm):
    """Форма добавления мнения"""
    title = StringField(
        'Введите название фильма',
        validators=[DataRequired(message="Обязательное поле"),
                    Length(1,128)]
    )
    text = TextAreaField(
        'Напишите мнение',
        validators=[DataRequired(message="Обязательное поле")],
    )
    source = URLField(
        'Добавьте ссылку на подробный обзор фильма',
        validators=[Length(1,256), Optional()]
    )
    submit = SubmitField('Добавить')