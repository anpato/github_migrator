from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from utils.socket import socket
from flask_socketio import SocketIO, emit
from resources.repo import Repos
from resources.org import Org
from utils import clone, create_repos, clear_dir
from engineio.payload import Payload
import time
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

Payload.max_decode_packets = 500

socket = SocketIO(app, cors_allowed_origins="*",
                  engineio_logger=True,
                  async_mode='threading',
                  ping_timeout=20,
                  logger=True, max_decode_packets=500)
api.add_resource(Repos, '/repos')
api.add_resource(Org, '/orgs')


@socket.on('connect')
def connected():
    print('Connected')


@socket.on('message')
def get_message(message):
    print(message)
    pass


@socket.on('disconnect')
def disconnect():
    print('Disconnected')


@socket.on('StartUpload', namespace='/upload')
def init_upload(message):
    dirname = os.getcwd()
    repos = message['repos']
    token = message['token']
    target = message['targetOrg']
    upload = clone(repos, target, token, dirname)
    create_repos(upload[0], token, target)
    emit('UploadProgress-{token}'.format(token=token), {"status": "Finished"})
    # clear_dir(upload[1])


if __name__ == '__main__':
    socket.run(app)
