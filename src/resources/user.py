from flask import Response, request
from database.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_restful import Resource
from mongoengine.errors import FieldDoesNotExist, NotUniqueError, DoesNotExist, ValidationError, InvalidQueryError

from resources.errors import SchemaValidationError, InternalServerError, DeletingUserError, UserNotExistsError

class UsersApi(Resource):
    def get(self):
        users = User.objects().only('id', 'name').to_json()
        return Response(users, mimetype="application/json", status=200)

class UserApi(Resource):
    @jwt_required()
    def put(self, id):
        try:
            body = request.get_json()
            User.objects.get(id=id).update(**body)
            return '', 200
        except InvalidQueryError:
            raise SchemaValidationError
        except Exception:
            raise InternalServerError

    @jwt_required()
    def delete(self, id):
        try:
            user_id = get_jwt_identity()
            user = User.objects.get(id=id)
            user.delete()
            return '', 200
        except Exception:
            raise InternalServerError
    def get(self, id):
        try:
            user = User.objects.only('id','name').get(id=id).to_json()
            return Response(user, mimetype="application/json", status=200)
        except DoesNotExist:
            raise UserNotExistsError
        except Exception:
            raise InternalServerError
