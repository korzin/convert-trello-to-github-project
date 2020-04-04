#!/usr/bin/env python

import copy
import json
import re
import requests
import sys

# class RestRespValidationException(Exception):
#     pass

TRELLO_BASIC_PATH = "https://api.trello.com"

# TODO add named program arguments
ARG_API_KEY = sys.argv[1]
ARG_AUTH_TOKEN = sys.argv[2]
ARG_SOURCE_BOARD_NAME = sys.argv[3]

FLOW_LIST_SCHEME = ["todo", "in progress", "done"]  # will be dynamic

def main():
    source_board_id = get_board_id_by_name(ARG_SOURCE_BOARD_NAME)
    all_source_lists = get_all_lists_by_board(source_board_id)
    lists_scheme = extract_as_lists_flow_scheme(all_source_lists)
    list_to_cards = get_lists_with_cards(lists_scheme)
    print("print dictionary: lists to casds. \n" + str(list_to_cards))

def get_lists_with_cards(listsByPattern):
    ordered_lists = []
    for key, lists in listsByPattern.items():
        ordered_lists.extend(lists)
    list_name_to_cards = {}
    for list in ordered_lists:
        url = TRELLO_BASIC_PATH + "/1/lists/" + list['id'] + "/cards"
        headers = {"Accept": "application/json"}
        query = {}
        params = with_auth_params(query)

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=params
        )
        list_name_to_cards[list['name']] = json.loads(response.text)
    return list_name_to_cards


def extract_as_lists_flow_scheme(board_lists):
    export_lists_dictionary = {}
    for name_pattern in FLOW_LIST_SCHEME:
        export_lists_dictionary[name_pattern] = []

    for list in board_lists:
        for name_pattern in FLOW_LIST_SCHEME:
            if re.search(name_pattern, list['name'], re.IGNORECASE):
                export_lists_dictionary[name_pattern].append(list)
                break

    return export_lists_dictionary


def get_all_lists_by_board(board_id):
    url = TRELLO_BASIC_PATH + "/1/boards/" + board_id + "/lists"
    headers = {"Accept": "application/json"}
    query = {}
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

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=params
    )
    # TODO extract
    if not hasattr(response, 'text'):
        print("err. Response has no body. :" + str(response))
        return

    boards_id_name_pairs = json.loads(response.text)
    source_board_id_name_pair = next((board for board in boards_id_name_pairs
                                      if name == board['name'])
                                     , None)

    if (source_board_id_name_pair is None):
        print("err. board not found")
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
