#!/bin/python

from bs4 import BeautifulSoup
import os
import sys
import pyperclip
import re
from urllib.parse import urlparse
import urllib.parse
import hashlib



"""
Script to scroll to next anchor in page.


TODO: Create a tempfile containing the anchors so that the list of anchors is only generated once

"""

def get_anchors_from_file(html_file):
    soup = BeautifulSoup(open(html_file), 'html.parser')
    ids = []
    
    # for tag in soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
    for tag in soup.find_all(['h1', 'h2', 'h3']):
        if tag.get('id'):
            ids.append(tag['id'])
            
    return ids

def get_anchors():
    clean_url = os.environ["QUTE_URL"].split("#")[0]
    hash_object = hashlib.sha256()
    hash_object.update(clean_url.encode('utf-8'))
    url_hash = hash_object.hexdigest()

    if os.path.isfile(f"/tmp/{url_hash}"):
        with open(f"/tmp/{url_hash}", "r") as f:
            ids = [line.strip() for line in f.readlines()]
        print("Read from file")
        print(ids)
    else:
        ids = get_anchors_from_file(os.environ["QUTE_HTML"])
        with open(f"/tmp/{url_hash}", "w") as f:
            f.write("\n".join(ids))
    return ids


def get_anchor(anchor_ids, n=1, loop=True):
    """
    n = how many to add/take away
    """

    anchor = ""
    if "#" in os.environ["QUTE_URL"]:
        parsed_url = urlparse(os.environ["QUTE_URL"])
        anchor = urllib.parse.unquote(parsed_url.fragment)
        print(anchor)

    next_anchor_index = 0

    if anchor in anchor_ids:
        current_anchor_index = anchor_ids.index(anchor)
        if not loop and ((current_anchor_index == 0 and n < 0) or (current_anchor_index == len(anchor_ids)-1 and n > 0)):
            exit()
        elif not loop:
            if n > 0: next_anchor_index = min(current_anchor_index + n, len(anchor_ids) - 1)
            elif n < 0: next_anchor_index = max(current_anchor_index + n, 0)
        elif loop: next_anchor_index = (current_anchor_index+n)%len(anchor_ids)

        if next_anchor_index == current_anchor_index: exit()
        #
        # if current_anchor_index + n <= len(ids) and current_anchor_index + n >= 0:
        #     next_anchor_index = current_anchor_index + n
        # elif current_anchor_index + n == len(ids):
        #     if loop: next_anchor_index = (current_anchor_index+n)%len(ids)
        #     else: exit()
        # elif current_anchor_index + n > len(ids):
        #     if loop: next_anchor_index = (current_anchor_index+n)%len(ids)
        #     else: next_anchor_index = len(ids) - 1
        # elif current_anchor_index == 0 and n < 0:
        #     if loop: next_anchor_index = (current_anchor_index+n)%len(ids)
        #     else: exit()
        # elif current_anchor_index + n < 0:
        #     if loop: next_anchor_index = (current_anchor_index+n)%len(ids)
        #     else: next_anchor_index = len(ids) - 1
        # else:
        #     next_anchor_index = current_anchor_index + 1
    return next_anchor_index

n = int(sys.argv[1]) if len(sys.argv) > 1 else 1
count = int(os.environ["QUTE_COUNT"]) if "QUTE_COUNT" in os.environ else 1
n *= count
os.system(f"notify-send 'Count {count}, {type(count)}'")

anchor_ids = get_anchors()
if not anchor_ids: exit()

next_anchor_index = get_anchor(anchor_ids, n=n, loop=True)


with open(os.environ["QUTE_FIFO"], "w") as f:
    f.write(f"scroll-to-anchor {anchor_ids[next_anchor_index]}")
