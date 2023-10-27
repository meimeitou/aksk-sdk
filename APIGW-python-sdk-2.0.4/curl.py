#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
import requests
import calendar
import time
import random
import string
import hmac
import hashlib
import argparse
import sys
from urllib.parse import urlparse
import json
from apig_sdk import signer

x_auth_expire_second = "120"

def get_random_string(length)-> str:
    result_str = ''.join(random.choice(string.ascii_letters) for i in range(length))
    return result_str

def curlv1(method, url, body):
    x_auth_accesskey = "apigateway_sdk_demo_key"
    auth_secret = "apigateway_sdk_demo_secret"
    p = urlparse(url)
    current_GMT = time.gmtime()
    timestamp = calendar.timegm(current_GMT)
    x_auth_random_str = get_random_string(8)

    content = f'{method.upper()}\n{p.path}\n{x_auth_accesskey}\n{x_auth_expire_second}\n{x_auth_random_str}\n{timestamp}'
    signature = hmac.new(bytes(auth_secret , 'utf-8'), msg = bytes(content , 'utf-8'), digestmod = hashlib.sha256).hexdigest()
    headers = {
        'x-auth-accesskey': x_auth_accesskey,
        "x-auth-version": "v1",
        "x-auth-timestamp": f'{timestamp}',
        "x-auth-expire-second": x_auth_expire_second,
        "x-auth-signature": signature,
        "x-auth-random-str": x_auth_random_str,
        'content-type': 'application/json'
    }
    data = {}
    if body:
        data = json.loads(body)
    if method.upper() == "GET":
        return requests.get(f'{url}', headers=headers, params=data)
    elif  method.upper() == "POST":
        return requests.post(f'{url}', headers=headers, json=data)

def curlv2(method, url, body):
    sig = signer.Signer()
    # Set the AK/SK to sign and authenticate the request.

    sig.Key = "apigateway_sdk_demo_key"
    sig.Secret = "apigateway_sdk_demo_secret"
    # The following example shows how to set the request URL and parameters to query a VPC list.
    # Set request Endpoint.
    # Specify a request method, such as GET, PUT, POST, DELETE, HEAD, and PATCH.
    # Set request URI.
    # Set parameters for the request URL.
    r = signer.HttpRequest(method.upper(), url)
    # Add header parameters, for example, x-domain-id for invoking a global service and x-project-id for invoking a project-level service.
    r.headers = {"content-type": "application/json"}
    # Add a body if you have specified the PUT or POST method. Special characters, such as the double quotation mark ("), contained in the body must be escaped.
    r.body = body
    sig.Sign(r)
    print(r.headers["X-Sdk-Date"])
    print(r.headers["Authorization"])
    resp = requests.request(r.method, r.scheme + "://" + r.host + r.uri, headers=r.headers, data=r.body)
    print(resp.status_code, resp.reason)
    print(resp.content.decode("utf-8"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='aksk curl')
    parser.add_argument('-m', '--method', type=str,
                    help='method',default="get")
    parser.add_argument('-u', '--url', type=str,
                    help='url',required=True)
    parser.add_argument('-b', '--body', type=str,
                    help='body',required=False, default='')
    parser.add_argument('-v', '--version', type=str,
                    help='version',default="v2")
    args = parser.parse_args()
    print(args.method, args.url, args.body)
    r = None
    if args.version == "v1":
        r=curlv1(args.method,  args.url, args.body)
        print(r.request.headers)
        print(r.status_code,r.content.decode("utf-8"))
    elif args.version == "v2":
        r=curlv2(args.method,  args.url, args.body)
    else:
        print("err version")
        exit(0)
    