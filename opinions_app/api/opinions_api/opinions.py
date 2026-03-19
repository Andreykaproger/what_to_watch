from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import current_user

from opinions_app import db
from opinions_app.models import Opinion, OpinionStatus
from opinions_app.opinions.routes import random_opinion
from opinions_app.error_handlers import InvalidAPIUsage
from opinions_app.schemas.opinions import UserOpinionSchema, UserOpinionsListSchema

from . import opinions_api_bp
from ...utils.decorators import active_user_required


@opinions_api_bp.route('/opinions', methods = ["GET"])
@opinions_api_bp.output(UserOpinionsListSchema)
def list_opinions():
    """Получение списка всех мнений"""
    opinions = Opinion.visible().all()

    return {
        "opinions": opinions
    }


@opinions_api_bp.route('/opinions/<int:id>/', methods = ["GET"])
@jwt_required(optional=True)
@opinions_api_bp.output(UserOpinionSchema)
def get_opinion(id):
    """Получение конкретного мнения по его id"""

    opinion = Opinion.query.get(id)

    if not (opinion and opinion.is_visible_to(current_user)):
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)

    return opinion


@opinions_api_bp.route("/opinions/random", methods = ["GET"])
@opinions_api_bp.output(UserOpinionSchema)
def get_random_opinion():
    """Получение случайного мнения"""

    opinion = random_opinion()

    if opinion is None:
        raise InvalidAPIUsage('В базе данных нет мнений', 404)

    return opinion


@opinions_api_bp.route('/opinions/create', methods = ["POST"])
@active_user_required()
@opinions_api_bp.input(UserOpinionSchema)
@opinions_api_bp.output(UserOpinionSchema)
def add_opinion(json_data):
    """Добавление нового мнения"""

    user_id = int(get_jwt_identity())

    if Opinion.query.filter_by(text=json_data['text']).first():
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных', 409)

    opinion = Opinion(**json_data, user_id = user_id)

    db.session.add(opinion)
    db.session.commit()

    return opinion


@opinions_api_bp.route('/opinions/<int:id>', methods = ["PATCH"])
@active_user_required()
@opinions_api_bp.input(UserOpinionSchema(partial=True))
@opinions_api_bp.output(UserOpinionSchema)
def update_opinion(json_data, id):
    """Редактирование мнения"""

    user_id = int(get_jwt_identity())
    opinion = Opinion.query.get(id)

    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)

    if user_id != opinion.user_id:
        raise InvalidAPIUsage("Это не ваше мнение!", 403)

    if 'text' in json_data:
        if Opinion.query.filter_by(text=json_data['text']).first():
            raise InvalidAPIUsage('Такое мнение уже существует', 400)

    opinion.title = json_data.get('title', opinion.title)
    opinion.text = json_data.get('text', opinion.text)
    opinion.source = json_data.get('source', opinion.source)

    opinion.status = OpinionStatus.PENDING

    db.session.commit()

    return opinion


@opinions_api_bp.route('/opinions/<int:id>', methods = ["DELETE"])
@active_user_required()
def delete_opinion(id):
    """Удаления мнения"""

    user_id = int(get_jwt_identity())
    opinion = Opinion.query.get(id)

    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)

    if user_id != opinion.user_id:
        raise InvalidAPIUsage("Это не ваше мнение!", 403)


    db.session.delete(opinion)
    db.session.commit()

    return "", 204


@opinions_api_bp.route('/users/me/opinions', methods = ["GET"])
@active_user_required()
@opinions_api_bp.output(UserOpinionSchema(many=True))
def user_opinions():
    """Показывает все мнения текущего пользователя"""

    user_id = int(get_jwt_identity())

    opinions = Opinion.query.filter_by(user_id = user_id).all()

    return opinions
