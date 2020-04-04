#!/usr/bin/env python

import copy
import json
import requests
import sys

# class RestRespValidationException(Exception):
#     pass

TRELLO_BASIC_PATH = "https://api.trello.com"

# TODO add named program arguments
ARG_API_KEY = sys.argv[1]
ARG_AUTH_TOKEN = sys.argv[2]
ARG_SOURCE_BOARD_NAME = sys.argv[3]


def main():
    source_board_id = get_board_id_by_name(ARG_SOURCE_BOARD_NAME)
    source_board = get_board_by_id(source_board_id)
    print("board: " + str(source_board))


def get_board_by_id(board_id):
    url = TRELLO_BASIC_PATH + "/1/members/me/boards/"
    headers = {"Accept": "application/json"}
    query = {"id": board_id}
    params = with_auth_params(query)

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=params
    )
    # TODO validate success response

    return json.loads(response.text)


def get_board_id_by_name(name):
    url = TRELLO_BASIC_PATH + "/1/members/me/boards"
    headers = {"Accept": "application/json"}
    query = {'fields': 'id,name'}
    params = with_auth_params(query)

    print(params)
    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=params
    )
    # TODO extract
    if not hasattr(response, 'text'):
        print("Response has no body. :" + str(response))
        print("Exit")
        return

    boards_id_name_pairs = json.loads(response.text)
    source_board_id_name_pair = next((board for board in boards_id_name_pairs
                                      if name == board['name'])
                                     , None)

    if (source_board_id_name_pair is None):
        print("err. board not found")
        print("Exit")
        return

    return source_board_id_name_pair['id']


def with_auth_params(params):
    params_with_auth = copy.deepcopy(params)
    api_key = sys.argv[1]
    auth_token = sys.argv[2]
    params_with_auth['key'] = api_key
    params_with_auth['token'] = auth_token
    return params_with_auth


if __name__ == '__main__':
    main()
