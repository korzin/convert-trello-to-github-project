#!/usr/bin/env python

import copy
import json
import requests
import sys

trello_basic_path = "https://api.trello.com"


def main():
    url = trello_basic_path + "/1/members/me/boards"
    headers = {"Accept": "application/json"}
    query = {}
    params = with_auth_params(query)

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=params
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

def with_auth_params(params):
    params_with_auth = copy.deepcopy(params)
    api_key = sys.argv[1]
    auth_token = sys.argv[2]
    params_with_auth['key'] = api_key
    params_with_auth['token'] = auth_token
    return params_with_auth

if __name__ == '__main__':
    main()
