#!/usr/bin/python3
# -*- coding: utf-8 -*-

import socket
from http.client import HTTPConnection, HTTPException

DOCUMENTATION = '''
---
module: test_challenges
short_description: Tests Let's Encrypt web server challenges
description:
     - The M(test_challenges) module verifies a list of hosts can access acme challenges for Let's Encrypt.
options:
  hosts:
    description:
      - A list of hostnames/domains to test.
    required: true
    default: null
    type: list
  file:
    description:
      - The dummy filename in the URL to test.
    required: no
    default: ping.txt
  path:
    description:
      - The path to the challenges in the URL.
    required: no
    default: /.well-known/acme-challenge
author:
    - Scott Walkinshaw
'''

EXAMPLES = '''
# Example from Ansible Playbooks.
- test_challenges:
    hosts:
      - example.com
      - www.example.com
      - www.mydomain.com
'''

def get_status(host, path, file):
    try:
        conn = HTTPConnection(host)
        conn.request('HEAD', '/{0}/{1}'.format(path, file), None, {
            'User-Agent': 'Trellis Ansible test_challenges module'
        })
        res = conn.getresponse()
    except (HTTPException, socket.timeout, socket.error):
        raise
    else:
        return res.status

def main():
    module = AnsibleModule(
        argument_spec = dict(
            file  = dict(default='ping.txt'),
            hosts = dict(required=True, type='list'),
            path  = dict(default='.well-known/acme-challenge')
        )
    )

    hosts = module.params['hosts']
    path = module.params['path']
    file = module.params['file']

    failed_hosts = []
    errors = []

    for host in hosts:
        try:
            status = get_status(host, path, file)
        except (HTTPException, socket.timeout, socket.error) as err:
            failed_hosts.append("{0} (0)".format(host))
            errors.append("Error for {0}: {1} ({2})".format(host, err, type(err)))
        else:
            if int(status) != 200:
                failed_hosts.append("{0} ({1})".format(host, status))

    rc = int(len(failed_hosts) > 0)

    module.exit_json(
        changed=False,
        rc=rc,
        failed_hosts=failed_hosts,
        errors=errors
    )

from ansible.module_utils.basic import *
main()
