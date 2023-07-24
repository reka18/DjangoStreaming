import json


def safe_loads(thing: object, trunc: bool = False) -> str:
    if thing is None:
        return '{}'
    else:
        if trunc:
            return {"id": thing.id}
        return json.loads(thing.string())
