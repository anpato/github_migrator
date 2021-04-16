import requests
import json


class Github:
    base_url: str = "https://api.github.com"

    def gen_headers(self, auth_token: str):
        return {
            "Authorization": "token {token}".format(token=auth_token)
        }

    def get_orgs(self, page: int, limit: int, auth_token: str):
        headers = self.gen_headers(auth_token)
        url: str = '{base_url}/user/orgs?per_page={limit}&page={page}'.format(
            base_url=self.base_url, limit=limit, page=page)
        res = requests.get(url=url, headers=headers)
        return res.json()

    def get_org_repos(self, page: int, limit: int, org: str, auth_token: str):
        headers = self.gen_headers(auth_token)
        url: str = '{base_url}/orgs/{org}/repos?per_page={limit}&type=all&page={page}'.format(
            org=org, page=page, base_url=self.base_url, limit=limit)
        res = requests.get(url=url, headers=headers)
        return res.json()

    def get_total_repos(self, org: str, auth_token: str):
        headers = self.gen_headers(auth_token)
        url: str = "{base_url}/orgs/{org}".format(
            base_url=self.base_url, org=org)
        res = requests.get(url=url, headers=headers)
        results = res.json()
        total = results['total_private_repos'] + results['public_repos']
        return total

    def create_repo(self, params: dict, auth_token: str):
        headers: dict = self.gen_headers(auth_token)
        url: str = "{base_url}/orgs/{org}/repos".format(
            base_url=self.base_url, org=self.out_org)
        data = {**params, "org": self.out_org, "private": True}
        res = requests.post(url=url, data=json.dumps(data),
                            headers=headers)
        return res.json()
