import dataclasses


def opt_json(v):
    """
    :param: Must be @dataclass
    :return: 200: Value, or 400: None
    """
    if v is not None:
        return dataclasses.asdict(v)

    else:
        return '', 400
