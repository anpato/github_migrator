from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from resources.repo import Repos
from resources.org import Org
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__)
CORS(app)

env = os.getenv('ENVIRONMENT')

if env and env == 'production':
    app.env = env
else:
    app.debug = True
    app.env = 'development'

api = Api(app)

api.add_resource(Repos, '/repos')
api.add_resource(Org, '/orgs')


if __name__ == '__main__':
    app.run()
