import requests
import json


class Github:
    base_url: str = "https://api.github.com"

    def __init__(self, auth_token: str, src_org: str, out_org: str):
        self.auth_token = auth_token
        self.src_org = src_org
        self.out_org = out_org

    def gen_headers(self):
        return {
            "Authorization": "token {token}".format(token=self.auth_token)
        }

    def get_org_repos(self, page: int):
        headers = self.gen_headers()
        url: str = '{base_url}/orgs/{org}/repos?per_page=100&type=all&page={page}'.format(
            org=self.src_org, page=page, base_url=self.base_url)
        res = requests.get(url=url, headers=headers)
        return res.json()

    def get_total_repos(self):
        headers = self.gen_headers()
        url: str = "{base_url}/orgs/{org}".format(
            base_url=self.base_url, org=self.src_org)
        res = requests.get(url=url, headers=headers)
        results = res.json()
        total = results['total_private_repos'] + results['public_repos']
        return total

    def create_repo(self, params: dict):
        headers: dict = self.gen_headers()
        url: str = "{base_url}/orgs/{org}/repos".format(
            base_url=self.base_url, org=self.out_org)
        data = {**params, "org": self.out_org, "private": True}
        res = requests.post(url=url, data=json.dumps(data),
                            headers=headers)
        return res.json()
