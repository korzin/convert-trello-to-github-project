#!/usr/bin/env python

import requests
import sys
import json

trello_basic_path = "https://api.trello.com"

def main():
    api_key = sys.argv[1]
    auth_token = sys.argv[2]

    url = trello_basic_path + "/1/members/me/boards"
    headers = {"Accept": "application/json"}
    query = {
        'key': api_key, 'token': auth_token
    }

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=query
    )

    print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))

if __name__ == '__main__':
    main()
