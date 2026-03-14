from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from opinions_app import db
from opinions_app.models import Opinion
from opinions_app.opinions.routes import random_opinion
from opinions_app.error_handlers import InvalidAPIUsage
from opinions_app.schemas import AddOpinionSchema, OpinionOutputSchema

from . import opinions_api_bp


@opinions_api_bp.route('/opinions/', methods = ["GET"])
@opinions_api_bp.output(list[OpinionOutputSchema])
def get_opinions():
    """Получение списка всех мнений"""

    opinions = Opinion.visible()
    opinions_list = [opinion.to_dict() for opinion in opinions]
    return jsonify({
        'opinions': opinions_list
    })

@opinions_api_bp.route('/opinions/<int:id>/', methods = ["GET"])
@opinions_api_bp.output(OpinionOutputSchema)
def get_opinion(id):
    """Получение конкретного мнения по его id"""

    opinion = Opinion.query.get(id)
    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)
    return jsonify({
        'opinion': opinion.to_dict()
    })

@opinions_api_bp.route("/get-random-opinion/", methods = ["GET"])
@opinions_api_bp.output(OpinionOutputSchema)
def get_random_opinion():
    """Получение случайного мнения"""

    opinion = random_opinion()
    if opinion is None:
        raise InvalidAPIUsage('В базе данных нет мнений', 404)
    return jsonify({
        'opinion': opinion.to_dict()
    })

@opinions_api_bp.route('/opinions/create/', methods = ["POST"])
@opinions_api_bp.input(AddOpinionSchema)
@jwt_required()
def add_opinion():
    """Добавление нового мнения"""

    user_id = int(get_jwt_identity())
    data = request.get_json()
    data["user_id"] = user_id

    if not('title' in data or 'text' in data):
        raise InvalidAPIUsage('В запросе отсутствуют обязательные поля')
    if Opinion.query.filter_by(text=data['text']).first() is not None:
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных')

    opinion = Opinion()
    opinion.from_dict(data)
    db.session.add(opinion)
    db.session.commit()

    return jsonify({
        'opinion': opinion.to_dict()
    })

@opinions_api_bp.route('/opinions/<int:id>/', methods = ["PATCH"])
@jwt_required()
def update_opinion(id):
    """Редактирование мнения"""

    user_id = int(get_jwt_identity())
    data = request.get_json()
    opinion = Opinion.query.get(id)

    if user_id != opinion.user_id:
        raise InvalidAPIUsage("Это не ваше мнение!", 403)

    if (
        'text' not in data and
        Opinion.query.filter_by(text=data['text']).first() is not None
    ):
        raise InvalidAPIUsage('Такое мнение уже есть в базе данных')


    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)

    opinion.title = data.get('title', opinion.title)
    opinion.text = data.get('text', opinion.text)
    opinion.source = data.get('source', opinion.source)
    db.session.commit()

    return jsonify({
        'opinion': opinion.to_dict()
    })

@opinions_api_bp.route('/opinions/<int:id>/', methods = ["DELETE"])
@jwt_required()
def delete_opinion(id):
    """Удаления мнения"""

    user_id = int(get_jwt_identity())
    opinion = Opinion.query.get(id)

    if user_id != opinion.user_id:
        raise InvalidAPIUsage("Это не ваше мнение!", 403)

    if opinion is None:
        raise InvalidAPIUsage('Мнение с указанным id не найдено', 404)

    db.session.delete(opinion)
    db.session.commit()
    return '', 204

@opinions_api_bp.route('/user-opinions', methods = ["GET"])
@jwt_required()
def user_opinions():
    user_id = int(get_jwt_identity())

    user_opinions = Opinion.query.filter_by(user_id = user_id).all()

    user_opinions_list = [user_opinion.to_dict() for user_opinion in user_opinions]

    return jsonify({
        "User opinions": user_opinions_list,
    })
