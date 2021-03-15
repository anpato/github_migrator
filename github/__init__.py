import requests

class Github:
    def __init__(self, auth_token:str, src_org:str, out_org:str):
        self.auth_token = auth_token
        self.src_org = src_org
        self.out_org = out_org

    def get_org(self):
        headers = {}

        res = requests.get('https://api.github.com/orgs/{org}/repos'.format(org=self.out_org))
        print(res.json())