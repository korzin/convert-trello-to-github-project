#!/usr/bin/env python

import json
import re
import requests
import sys
import time
from datetime import datetime

import http_util

# TODO add named program arguments
ARG_TRELLO_API_KEY = sys.argv[1]
ARG_TRELLO_AUTH_TOKEN = sys.argv[2]
ARG_SOURCE_BOARD_NAME = sys.argv[3]
ARG_TARGET_GITHUB_LOGIN = sys.argv[4]
ARG_TARGET_GITHUB_REPO = sys.argv[5]
ARG_TARGET_GITHUB_TOKEN = sys.argv[6]

TRELLO_BASIC_PATH = "https://api.trello.com"
GITHUB_BASIC_PATH = "https://api.github.com"

CURR_DATE = datetime.date(datetime.now())  # format 'yyyy-mm-dd'
FLOW_LIST_SCHEME = ["todo", "in progress", "done"]  # will be dynamic

def main():
    # TRELLO export
    print("Trello board \"" + ARG_SOURCE_BOARD_NAME + "\" export started...")
    source_board_id = trello_get_board_id_by_name(ARG_SOURCE_BOARD_NAME)
    all_source_lists = trello_get_all_lists_by_board(source_board_id)
    lists_scheme = trello_extract_as_lists_flow_scheme(all_source_lists)
    list_to_cards = trello_get_lists_with_cards(lists_scheme)
    print("Trello board \"" + ARG_SOURCE_BOARD_NAME + "\" export finished.")

    # GITHUB import
    print("Github project " + ARG_SOURCE_BOARD_NAME + "processing started...")
    github_create_and_fill_project_by_trello_cards_by_columns(
        list_to_cards)
    print("Github project " + ARG_SOURCE_BOARD_NAME + "processing finished.")


def github_create_column_by_name(project_id, column_name):
    url = GITHUB_BASIC_PATH + "/projects/" + str(project_id) + "/columns"
    headers = http_util.github_prepare_request_headers(ARG_TARGET_GITHUB_TOKEN)
    body = {"name": column_name}
    response = requests.post(url,
                             headers=headers,
                             data=json.dumps(body)
                             )
    create_column_response = json.loads(response.text)
    id_ = create_column_response["id"]
    print("log. created column \"" + column_name + "\" with id: " + str(id_))
    return id_


def github_create_and_fill_project_by_trello_cards_by_columns(list_to_cards):
    project_id = github_create_project()
    for column_name, trello_cards in list_to_cards.items():
        time.sleep(0.5)
        column_id = github_create_column_by_name(project_id, column_name)
        github_create_trello_cards_mirror(column_id, trello_cards)


def github_create_project():
    url = GITHUB_BASIC_PATH + "/repos/" + \
          ARG_TARGET_GITHUB_LOGIN + "/" + \
          ARG_TARGET_GITHUB_REPO + "/projects"

    headers = http_util.github_prepare_request_headers(ARG_TARGET_GITHUB_TOKEN)
    body = {"name": ARG_SOURCE_BOARD_NAME,
            "body": "Created automatically. It is mirror of trello board on " + str(
                CURR_DATE)}

    response = requests.post(url, data=json.dumps(body), headers=headers)
    create_board_response = json.loads(response.text)
    id_ = create_board_response["id"]
    print("log. created project: " + str(id_))
    return id_


def github_create_trello_cards_mirror(column_id, trello_cards):
    url = GITHUB_BASIC_PATH + "/projects/columns/" + str(column_id) + "/cards"
    headers = http_util.github_prepare_request_headers(ARG_TARGET_GITHUB_TOKEN)
    create_cards_responses = []
    for trello_card in trello_cards:
        time.sleep(0.5)
        body = {
            "note": trello_card["name"]
        }
        response = requests.post(url,
                                 headers=headers,
                                 data=json.dumps(body)
                                 )
        create_card_response = json.loads(response.text)
        create_cards_responses.append(create_card_response)

    print("log. created " + str(
        len(create_cards_responses)) + " cards for column: " + str(column_id))


def trello_get_lists_with_cards(lists_by_pattern):
    ordered_lists = []
    for key, lists in lists_by_pattern.items():
        ordered_lists.extend(lists)
    list_name_to_cards = {}
    for list in ordered_lists:
        url = TRELLO_BASIC_PATH + "/1/lists/" + list['id'] + "/cards"
        headers = {"Accept": "application/json"}
        query = {}
        params = http_util.with_trello_auth_params(query, ARG_TRELLO_API_KEY,
                                                   ARG_TRELLO_AUTH_TOKEN)

        response = requests.request(
            "GET",
            url,
            headers=headers,
            params=params
        )
        list_name_to_cards[list['name']] = json.loads(response.text)
    return list_name_to_cards


def trello_extract_as_lists_flow_scheme(board_lists):
    export_lists_dictionary = {}
    for name_pattern in FLOW_LIST_SCHEME:
        export_lists_dictionary[name_pattern] = []

    for list in board_lists:
        for name_pattern in FLOW_LIST_SCHEME:
            if re.search(name_pattern, list['name'], re.IGNORECASE):
                export_lists_dictionary[name_pattern].append(list)
                break

    return export_lists_dictionary


def trello_get_all_lists_by_board(board_id):
    url = TRELLO_BASIC_PATH + "/1/boards/" + board_id + "/lists"
    headers = {"Accept": "application/json"}
    query = {}
    params = http_util.with_trello_auth_params(query, ARG_TRELLO_API_KEY,
                                               ARG_TRELLO_AUTH_TOKEN)

    response = requests.request(
        "GET",
        url,
        headers=headers,
        params=params
    )
    # TODO validate success response

    return json.loads(response.text)


def trello_get_board_id_by_name(name):
    url = TRELLO_BASIC_PATH + "/1/members/me/boards"
    headers = {"Accept": "application/json"}
    query = {'fields': 'id,name'}
    params = http_util.with_trello_auth_params(query, ARG_TRELLO_API_KEY,
                                               ARG_TRELLO_AUTH_TOKEN)

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


if __name__ == '__main__':
    main()
