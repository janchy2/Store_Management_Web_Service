from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from flask import jsonify, make_response

def roleCheck(role):
    def innerRole(function):
        @wraps(function)
        def decorator(*arguments, **keywordArguments):
            verify_jwt_in_request()
            claims = get_jwt()
            if("role" in claims and claims["role"] == role):
                return function(*arguments, **keywordArguments)
            else:
                response = jsonify(msg="Missing Authorization Header")
                return make_response(response, 401)

        return decorator

    return innerRole