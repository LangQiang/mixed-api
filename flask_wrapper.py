from flask import Flask
from json_response import JsonResponse
import json


class JsonFlask(Flask):
    def make_response(self, rv):
        if rv is None or isinstance(rv, (list, dict, bool, str, int, float)):
            rv = JsonResponse.success(rv)

        if isinstance(rv, JsonResponse):
            rv = json.dumps(rv.to_dict(), ensure_ascii=False)

        return super().make_response(rv)
