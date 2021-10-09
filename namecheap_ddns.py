#!/usr/bin/env python3

import sys
import argparse
import requests
from xml.etree import ElementTree

"""
Third party docs:
- https://www.namecheap.com/support/knowledgebase/article.aspx/29/11/how-to-dynamically-update-the-hosts-ip-with-an-http-request/
"""


def get_public_ip():
    return requests.get("https://api.ipify.org").content.decode("utf8")


def success():
    print("good")
    sys.exit(0)


def fail():
    print("badauth")
    sys.exit(-1)


def parse_args():
    parser = argparse.ArgumentParser(description="namecheap ddns updater")

    parser.add_argument("username", type=str, help="comma separated hostnames")
    parser.add_argument("password", type=str, help="ddns password")
    parser.add_argument("domain", type=str, help="domain name e.g example.co.uk")
    parser.add_argument(
        "ip",
        type=str,
        nargs="?",
        help="ip address e.g 182.34.0.22",
        default=get_public_ip(),
    )

    return parser.parse_args()


def update_ddns(*, host, domain, password, ip):
    """
    Success Response Example:
    <?xml version="1.0"?><interface-response><Command>SETDNSHOST</Command><Language>eng</Language><IP>108.21.57.47</IP><ErrCount>0</ErrCount><ResponseCount>0</ResponseCount><Done>true</Done><debug><![CDATA[]]></debug></interface-response>

    Error Response Example:
    <?xml version="1.0"?><interface-response><Command>SETDNSHOST</Command><Language>eng</Language><ErrCount>1</ErrCount><errors><Err1>Passwords do not match</Err1></errors><ResponseCount>1</ResponseCount><responses><response><ResponseNumber>304156</ResponseNumber><ResponseString>Validation error; invalid ; password</ResponseString></response></responses><Done>true</Done><debug><![CDATA[]]></debug></interface-response>
    """

    url = f"https://dynamicdns.park-your-domain.com/update?host={host}&domain={domain}&password={password}&ip={ip}"
    resp = requests.get(url)

    if resp.status_code == 200:
        root = ElementTree.fromstring(resp.content)
        err_count = int(root.find("ErrCount").text)
        if err_count == 0:
            return True

    return False


args = parse_args()

# interpret username as comma separated host list
hosts = args.username.split(",")

statuses = [
    update_ddns(host=host, domain=args.domain, password=args.password, ip=args.ip)
    for host in hosts
]

if not all(statuses):
    fail()

success()
