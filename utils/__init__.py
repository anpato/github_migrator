from github import Github
import math
from flask import request
import os
from flask_socketio import emit


def get_all(token, org, page, limit):
    gh = Github()
    total = gh.get_total_repos(org, token)
    total_pages = math.ceil(total / int(limit))
    src_repos = gh.get_org_repos(page, limit, org, token)
    return {"repos": src_repos, "total_pages": total_pages}


def clone(repos: list, target: str, token: str, dirname: str):
    storage_path = '{dirname}/{target}-repos'.format(
        dirname=dirname, target=target)
    cloned_repos = []
    if not os.path.isdir(storage_path):
        os.mkdir(storage_path)
    count = 1
    for repo in repos:
        try:
            cmd: str = "git -C {storage} clone {clone_url} -q".format(
                clone_url=repo['ssh_url'], storage=storage_path)
            os.system(cmd)
            path = "{storage}/{repo_name}".format(storage=storage_path,
                                                  repo_name=repo['name'])
            repo_data = {
                "path": path, "desc": repo['description'], "name": repo['name']}
            cloned_repos.append(repo_data)
        except Exception as error:
            print(error)

        emit('UploadProgress-{token}'.format(token=token), {"status": "Cloning",
                                                            "progress": count}, namespace='/upload')
        count += 1
    return (cloned_repos, storage_path)


def create_repos(repos: list, token: str, out_org: str):
    gh = Github()
    count = 1
    for r in repos:
        body = {
            "visibility": "private",
            "name": r['name'],
            "description": r["desc"]
        }
        try:
            res = gh.create_repo(body, token, out_org)
            clone_url = res['ssh_url']
            print("\n")
            cmd: str = "cd {dir} && git push -u --mirror -q {url}".format(
                dir=r['path'].replace('/app', ''), url=clone_url)
            os.system(cmd)
        except Exception as error:
            print(error)
        emit('UploadProgress-{token}'.format(token=token), {"status": "Creating",
                                                            "progress": count}, namespace='/upload')
        count += 1


def clear_dir(path):
    os.system('rm -rf {path}'.format(path=path))


def get_token():
    try:
        token = request.headers['Authorization'].split(' ')[1]
        return token
    except:
        return "No Token"
