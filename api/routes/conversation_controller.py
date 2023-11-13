import datetime

from flask import Blueprint, request
from sqlalchemy import func

from api.routes.controller_utils import opt_json, get_page_args
from api.storage import Storage
from image.dtos import ThreadDto, MessageDto

conversation_blueprint = Blueprint(name="conversation", import_name="conversation", url_prefix="/conversation")


@conversation_blueprint.route("/all")
def get_all_conversations():
    db = Storage.get_db()
    limit, page = get_page_args()
    pagination = db.pagination(entity=ThreadDto, per_page=limit, page=page)
    return opt_json(pagination)


@conversation_blueprint.route("/by-id/<id1>")
def get_conversation_by_id(id1: int):
    db = Storage.get_db()
    return opt_json(db.q(ThreadDto).filter_by(id=id1).first())


@conversation_blueprint.route("/<id1>/messages/desc")
def get_messages_by_id(id1: int):
    db = Storage.get_db()
    limit, page = get_page_args(def_total=50)
    pagination = db.pagination(entity=MessageDto,
                               per_page=limit,
                               page=page,
                               additional_steps=lambda q: q.filter_by(thread_id=id1).order_by(
                                   MessageDto.sent_at.desc()))
    return opt_json(pagination)


@conversation_blueprint.route("/<id1>/messages/search")
def search_messages_by_content(id1: int):
    db = Storage.get_db()
    limit, page = get_page_args(def_total=10)
    content = request.args.get("content", default=None, type=str)
    pag = db.pagination(entity=MessageDto,
                        per_page=limit,
                        page=page,
                        additional_steps=lambda q: q.filter_by(thread_id=id1).filter(MessageDto.content.like(f"%{content}%")))
    return opt_json(pag)


@conversation_blueprint.route("/<id1>/messages/by-date")
def search_messages_by_date(id1: int):
    db = Storage.get_db()
    date = datetime.date.fromisoformat(request.args.get("date", default=None))
    limit, page = get_page_args(def_total=50)
    pag = db.pagination(entity=MessageDto,
                        per_page=limit,
                        page=page,
                        additional_steps=lambda q: q.filter_by(thread_id=id1).filter(func.extract("day", MessageDto.sent_at) == date.day))
    return opt_json(pag)


def __get_message_dto_page_number(conversation_id: int, message_id: int, page_size: int = 50) -> int:
    db = Storage.get_db()
    row_number_query = (
        db.q(MessageDto)
        .filter_by(thread_id=conversation_id)
        .with_entities(MessageDto.id, func.row_number().over(order_by=MessageDto.sent_at.desc()).label('row_number'))
        .subquery()
    )
    paginated_query = (
        db.q(row_number_query).filter(row_number_query.c.id == message_id)
    )
    row_number = paginated_query.first()[1]
    return row_number // (page_size + 1)


@conversation_blueprint.route("/<conversation_id>/messages/<message_id>/page_number")
def get_page_number(conversation_id: int, message_id: int):
    limit = request.args.get("limit", default=25, type=int)
    return str(__get_message_dto_page_number(conversation_id, message_id, page_size=limit))
