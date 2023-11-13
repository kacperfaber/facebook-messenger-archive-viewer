import dataclasses

from flask import request


def opt_json(v):
    """
    :param: Must be @dataclass
    :return: 200: Value, or 400: None
    """
    if v is not None:
        return dataclasses.asdict(v)

    else:
        return '', 400


def get_page_args(def_total=10, def_page=0) -> (int, int):
    """
    :param def_total: Default 'total'
    :param def_page: Default 'page'
    :return: (total: int, page: int)
    """
    total = request.args.get("total", default=def_total, type=int)
    page = request.args.get("page", default=def_page, type=int)
    return total, page
