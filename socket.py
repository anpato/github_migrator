from flask import Flask
from utils import clone, create_repos, clear_dir
from utils.socket import socket
from flask_socketio import SocketIO, emit

app = Flask(__name__)


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
    repos = message['repos']
    token = message['token']
    target = message['targetOrg']
    upload = clone(repos, target, token)
    create_repos(upload[0], token, target)
    emit('UploadProgress-{}'.format(token), {"status": "Finished"})
    clear_dir(upload[1])


if __name__ == '__main__':
    socket.init_app(app, cors_allowed_origins='*')
