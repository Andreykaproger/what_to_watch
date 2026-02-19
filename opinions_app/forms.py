from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, URLField, SubmitField, EmailField
from wtforms.fields.simple import PasswordField
from wtforms.validators import DataRequired, Length, Optional, EqualTo, Email


class RegisterForm(FlaskForm):
    username = StringField(
        'Введите никнейм',
        validators= [
            DataRequired(message='Обязательное поле'),
            Length(3,64)
        ]
    )
    email = StringField(
        'Введите адрес электронной почты',
        validators= [
            DataRequired('Обязательное поле'),
            Email('Неверная форма E-Mail'),
        ]
    )
    password = PasswordField(
        'Введите пароль',
        validators= [
            DataRequired('Обязательное поле'),
            Length(6,128),
        ]
    )
    confirm_password = PasswordField(
        'Подтвердите пароль',
        validators= [
            DataRequired('Обязательное поле'),
            EqualTo('password')
        ]
    )
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    email = StringField(
        'Введите адрес электронной почты',
        validators= [
            DataRequired('Обязательное поле'),
            Email('Неверная форма E-Mail'),
        ]
    )
    password = PasswordField(
        'Введите пароль',
        validators= [
            DataRequired('Обязательное поле'),
            Length(6,128),
        ]
    )
    submit = SubmitField('Войти')

class OpinionForm(FlaskForm):
    """Форма добавления мнения"""
    title = StringField(
        'Введите название фильма',
        validators=[DataRequired(message="Обязательное поле"),
                    Length(1,128)]
    )
    text = TextAreaField(
        'Напишите мнение',
        validators=[DataRequired(message="Обязательное поле"),
                    Length(1,)],
    )
    source = URLField(
        'Добавьте ссылку на подробный обзор фильма',
        validators=[Length(1,256), Optional()]
    )
    submit = SubmitField('Добавить')