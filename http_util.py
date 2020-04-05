#!/usr/bin/env python

import copy


def github_prepare_request_headers(github_token):
    headers = {
        "Accept": "application/vnd.github.inertia-preview+json",
        "Authorization": "token " + github_token
    }
    return headers


def with_trello_auth_params(params, api_key, api_token):
    params_with_auth = copy.deepcopy(params)
    params_with_auth['key'] = api_key
    params_with_auth['token'] = api_token
    return params_with_auth
