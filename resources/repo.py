from flask_restful import Resource
from flask import request, Response
from utils import get_all, get_token, clone, create_repos
from utils.socket import socket
from flask_socketio import emit
import time


class Repos(Resource):
    def get(self):
        args = request.args
        oauth_key = get_token()
        if not args:
            return {"msg": "No Args Provided"}, 400
        org_name = args['org_name']
        page = args['page']
        limit = args['limit']
        if int(limit) > 50:
            return {"msg": "Limit Is Not Allowed"}, 400
        repos = get_all(oauth_key, org_name, page, limit)
        return repos
