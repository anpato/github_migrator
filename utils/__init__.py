from github import Github
import math
from flask import request
import threading


def get_all(token, org, page, limit):
    gh = Github()
    total = gh.get_total_repos(org, token)
    total_pages = math.ceil(total / int(limit))
    repo_list = []
    src_repos = gh.get_org_repos(page, limit, org, token)
    return {"repos": src_repos, "total_pages": total_pages}


def clone(repos: list, response, token: str):
    storage_path = './{token}-repos'.format(token)
    cloned_repos = []
    if not os.path.isdir(storage_path):
        os.mkdir(storage_path)
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
        except:
            pass
    return cloned_repos


def create_repos(repos: list, token: str):
    bar = Bar('Creating and Pushing Repos', max=len(repos))
    for r in repos:
        body = {
            "visibility": "private",
            "name": r['name'],
            "description": r["desc"]
        }
        try:
            res = gh.create_repo(body)
            clone_url = res['ssh_url']
            print("\n")
            cmd: str = "cd {dir} && git push -u --mirror -q {url}".format(
                dir=r['path'], url=clone_url)
            os.system(cmd)
        except:
            pass
        bar.next()
    bar.finish()


def clear_dir():
    print('Clearing Repos')
    os.system('rm -rf ./repos')


def get_token():
    try:
        token = request.headers['Authorization'].split(' ')[1]
        return token
    except:
        return "No Token"


class Thread(threading.Thread):
    def __init__(self):
        self.progress = 0
        super().__init__()

    def run(self, curren: int, total: int, cb, args):
        return cb(args)
