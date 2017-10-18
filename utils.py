from collections import namedtuple
import json


class Utils:
    @staticmethod
    def json2obj(content):
        json_correct = json.dumps(content, ensure_ascii=False)
        return json.loads(json_correct, object_hook=lambda d: namedtuple('object', d.keys())(*d.values()))
