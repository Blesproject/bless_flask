from flask_restful import Resource, reqparse, fields
from app.helpers.rest import *
# from app.helpers.memcache import *
from app.middlewares.auth import jwt_required
import datetime
from app.models import model as db


class UserdataResource(Resource):
    @jwt_required
    def get(self):
        obj_userdata = list()
        
        try:
            results = db.get_all("tb_userdata")
        except Exception:
            return response(200, message="Users Data Not Found")
        else:
            for i in results :
                data = {
                    "id_userdata": str(i['id_userdata']),
                    "email" : i['email'],
                    "first_name" : i['first_name'],
                    "last_name" : i['last_name'],
                    "location" : i['location'],
                    "city" : i['city'],
                    "province" : i['province'],
                    "created_at": str(i['created_at'])
                }
                obj_userdata.append(data)
            return response(200, data=obj_userdata)


class UserdataResourceById(Resource):
    @jwt_required
    def get(self, id_userdata):
        obj_userdata = []
        results = db.get_by_id(
                    table="tb_userdata",
                    field="id_userdata",
                    value=id_userdata
                )

        for i in results :
            data = {
                "id_userdata": str(i['id_userdata']),
                "email" : i['email'],
                "first_name" : i['first_name'],
                "last_name" : i['last_name'],
                "location" : i['location'],
                "city" : i['city'],
                "province" : i['province'],
                "created_at": str(i['created_at'])
            }
            obj_userdata.append(data)
        return response(200, data=obj_userdata)


class UserdataInsert(Resource):
    # @jwt_required
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('location', type=str, required=True)
        parser.add_argument('city', type=str, required=True)
        parser.add_argument('province', type=str, required=True)
        args = parser.parse_args()

        data_insert = {
            "email" : args['email'],
            "first_name" : args['first_name'],
            "last_name" : args['last_name'],
            "location" : args['location'],
            "city" : args['city'],
            "province" : args['province']
        }
        try:
            result = db.insert(table="tb_userdata", data=data_insert)
        except Exception as e:
            message = {
                "status": False,
                "error": str(e)
            }
        else:
            message = {
                "status": True,
                "data": data_insert,
                "id": result
            }
        finally:
            return response(200, message=message,)


class UserdataRemove(Resource):
    @jwt_required
    def delete(self, id_userdata):
        try:
            db.delete(
                    table="tb_userdata", 
                    field='id_userdata',
                    value=id_userdata
                )
        except Exception as e:
            message = {
                "status": False,
                "error": str(e)
            }
        else:
            message = "removing"

        finally:
            return response(200, message=message)


class UserdataUpdate(Resource):
    @jwt_required
    def put(self, id_userdata):
        parser = reqparse.RequestParser()
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        parser.add_argument('location', type=str, required=True)
        parser.add_argument('city', type=str, required=True)
        parser.add_argument('province', type=str, required=True)
        args = parser.parse_args()

        data = {
            "where":{
                "id_userdata": id_userdata
            },
            "data":{
                "email" : args['email'],
                "first_name" : args['first_name'],
                "last_name" : args['last_name'],
                "location" : args['location'],
                "city" : args['city'],
                "province" : args['province']
            }
        }

        
        try:
            db.update("tb_userdata", data=data)
        except Exception as e:
            message = {
                "status": False,
                "error": str(e)
            }
        else:
            message = {
                "status": True,
                "data": data
            }
        finally:
            return response(200, message=message)

