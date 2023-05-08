#!/usr/bin/env python

# Source: https://gitlab.com/gitlab-com/marketing/corporate_marketing/developer-evangelism/code/docker-hub-limit-exporter

# Info: Prometheus Exporter to fetch the Docker Hub Rate Limits metrics
# License: MIT, Copyright (c) 2020-present GitLab B.V.
# Author: Michael Friedrich <mfriedrich@gitlab.com>

import time
import requests
import json
import os
import jwt
from prometheus_client.core import GaugeMetricFamily, REGISTRY
from prometheus_client import start_http_server

VERSION = '1.0.0'

def print_headers(headers):
    print("HTTP Headers START")
    print('\r\n'.join('{}: {}'.format(k, v) for k, v in headers.items()),)
    print("HTTP Headers END")

class DockerHubCollector(object):
    def __init__(self, verbose, username, password):
        self.repository = 'ratelimitpreview/test'
        self.token_url = 'https://auth.docker.io/token?service=registry.docker.io&scope=repository:' + self.repository + ':pull'
        self.registry_url = 'https://registry-1.docker.io/v2/' + self.repository + '/manifests/latest'
        self.username = username
        self.password = password

        self.verbose = verbose
        
        self.previous_limit = None
        self.previous_remaining = None

    def do_verbose(self, text):
        if self.verbose:
            print("Notice: " + text)

    def limit_extractor(self, str_raw):
        self.do_verbose("Extracting limit from string: " + str(str_raw))

        if ";" in str_raw:
            split_arr = str_raw.split(';') # TODO: return the duration window too
            if len(split_arr) > 0:
                return split_arr[0]
        else:
            return str_raw

    def get_token(self):
        # User has passed in own credentials, or we need anonymous access.
        if self.username and self.password:
            r_token = requests.get(self.token_url, auth=(self.username, self.password))

            self.do_verbose("Using Docker Hub credentials for '" + self.username + "'")
        else:
            r_token = requests.get(self.token_url)

            self.do_verbose("Using anonymous Docker Hub token")

        # error handling
        r_token.raise_for_status()

        resp_token = r_token.json()

        self.do_verbose("Response token:'" + json.dumps(resp_token) + "'")

        token = resp_token.get('token')

        if not token:
            raise Exception('Cannot obtain token from Docker Hub. Please try again!')

        # extract content from jwt token
        jwtContent = jwt.decode(token, options={"verify_signature": False})
        if not self.previous_limit:
            self.previous_limit = jwtContent.get('access')[0].get('parameters').get('pull_limit')
            self.previous_remaining = self.previous_limit

        return token

    ## Test against registry
    def get_registry_limits(self):
        headers_registry = { 'Authorization': 'Bearer ' + self.get_token() }

        # Use a HEAD request to fetch the headers and avoid a decreased pull count
        r_registry = requests.head(self.registry_url, headers=headers_registry)

        # error handling
        r_registry.raise_for_status()

        # We need to check the response headers!
        resp_headers = r_registry.headers

        if self.verbose:
            print_headers(resp_headers)

        # TODO: Figure out what to return when the headers are missing for some reason.
        limit = 0
        remaining = 0
        reset = 0

        if "RateLimit-Limit" in resp_headers and "RateLimit-Remaining" in resp_headers:
            limit = self.limit_extractor(resp_headers["RateLimit-Limit"])
            remaining = self.limit_extractor(resp_headers["RateLimit-Remaining"])

        if "RateLimit-Reset" in resp_headers:
            reset = self.limit_extractor(resp_headers["RateLimit-Reset"])

        return (limit, remaining, reset)

    def collect(self):
        (limit, remaining, reset) = self.get_registry_limits()

        if len(str(remaining)) == 0:
            remaining = self.previous_remaining
        else:
            self.previous_remaining = remaining

        gr = GaugeMetricFamily("dockerhub_limit_remaining_requests_total", 'Docker Hub Rate Limit Remaining Requests', labels=['limit'])
        gr.add_metric(["remaining_requests_total"], remaining)

        yield gr

        if len(str(limit)) == 0:
            limit = self.previous_limit
        else:
            self.previous_limit = limit

        gl = GaugeMetricFamily("dockerhub_limit_max_requests_total", 'Docker Hub Rate Limit Maximum Requests', labels=['limit'])
        gl.add_metric(["max_requests_total"], limit)

        yield gl

if __name__ == '__main__':

    port = os.environ.get('DOCKERHUB_EXPORTER_PORT')

    if not port:
        port = 80

    start_http_server(int(port),addr='::')

    verbose = os.environ.get('DOCKERHUB_EXPORTER_VERBOSE')

    if not verbose:
        verbose = False

    username = os.environ.get('DOCKERHUB_USERNAME')
    password = os.environ.get('DOCKERHUB_PASSWORD')

    dhc = DockerHubCollector(bool(verbose), username, password)

    REGISTRY.register(dhc)

    while True:
        time.sleep(10)
        dhc.collect()
