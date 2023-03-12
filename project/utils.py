import json


def read_json(filename: str, encoding: str = "utf-8") -> list | dict:
    with open(filename, encoding=encoding) as f:
        return json.load(f)