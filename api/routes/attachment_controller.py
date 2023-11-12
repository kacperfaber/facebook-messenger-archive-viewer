from flask import Blueprint, current_app, request

from api.routes.controller_utils import opt_json
from api.storage import Storage
from image.db import Db
from image.dtos import AttachmentDto

attachment_blueprint = Blueprint(name="attachment", import_name="attachment", url_prefix="/attachment")


@attachment_blueprint.route("/by-path")
def get_attachment_by_id() -> AttachmentDto:
    path = request.args.get("path")
    return opt_json(Storage.get_db().q(AttachmentDto).filter_by(path=path).first())
