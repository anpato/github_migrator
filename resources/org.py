from flask_restful import Resource
from flask import request
from github import Github
from utils import get_token


class Org(Resource):
    def get(self):
        gh = Github()
        token = get_token()
        args = request.args
        page = args['page']
        limit = args['limit']
        orgs = gh.get_orgs(page, limit, token)
        return orgs
