from github import Github
import math
import os
from progress.bar import Bar
from dotenv import load_dotenv

TOKEN = os.getenv('GITHUB_TOKEN')


src_org = input("What org are you forking from? \n Org Name: ")
out_org = input("What org are your forking to? \n Org Name: ")
if TOKEN == None:
    TOKEN = input("Enter your personal access token. You can generate one with these instructions:https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token \n Your Token: ")
wants_save_token = input(
    "Would you like to save your token for later use? (y/n): ")

if wants_save_token:
    cmd: str = 'touch .env && echo "GITHUB_TOKEN={token}" >> .env'.format(
        token=TOKEN)
    os.system(cmd)

gh = Github(TOKEN, src_org, out_org)


total = gh.get_total_repos()
total_pages = math.ceil(total / 100)


def get_all():
    repo_list = []
    page = 1
    bar = Bar('Retrieving Repos', max=total_pages)
    while page < total_pages + 1:
        src_repos = gh.get_org_repos(page)
        repo_list = [*repo_list, *src_repos]
        page += 1
        bar.next()
    bar.finish()
    return repo_list


def clone(repos: list):
    storage_path = './repos'
    bar = Bar('Cloning Repos', max=len(repos))
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

        bar.next()
    bar.finish()
    return cloned_repos


def create_repos(repos: list):
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


if __name__ == 'main':
    repos = get_all()
    cloned_repos = clone(repos)
    create_repos(cloned_repos)
    clear_dir()
    print('Done, Enjoy your new repos on {out}! \N{grinning face}'.format(
        out=out_org))
