from opinions_app.models import User
from opinions_app import db


def register_user(username, email, password):

    if User.query.filter_by(email=email).first():
        return None, "Такой email уже зарегистрирован!"

    if User.query.filter_by(username=username).first():
        return None, "Такое имя уже существует!"

    user = User(
        username=username,
        email=email
    )
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    return user, None

def authenticate_user(email, password):

    user = User.query.filter_by(email=email).first()

    if not user:
        return None, "Неверный email или пароль"

    if not user.is_active:
        return None, f"Ваш аккаунт заблокирован по причине {user.block_reason}"

    if not user.check_password(password):
        return None, "Неверный email или пароль"

    return user, None