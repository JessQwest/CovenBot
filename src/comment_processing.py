import shlex # parse string like shell line
import re # regular expressions
import time

from global_vars import mod_list, regions, subregions
from db import insert_irl_record
from wiki import build_irl_wiki

def process_comment(comment):
    author = comment.author
    is_mod = author in mod_list
    start_with_exclamation = comment.body.startswith("!")
    print(f"\nComment found ({comment}): {comment.body[:100]}")
    print(f"Author: {comment.author}. Is Mod:{is_mod}. Exclamation: {start_with_exclamation}")
    if is_mod == False or start_with_exclamation == False:
        print("Comment does not meet criteria. Ignoring...")
        return
    print("Comment meets criteria. Processing...")
    if comment.body.startswith("!irl"):
        parse_irl(comment)
    elif comment.body.startswith("!online"):
        parse_online(comment)
    else:
        print("Comment does not match any command. Sending Mod Mail...")


def parse_irl(comment):
    print("Parsing IRL comment")
    tokens = shlex.split(comment.body, posix=False)
    print(f"Tokens: {tokens}")
    if not tokens:
        print("No tokens found. Ignoring")
        return
    tokens.pop(0)

    post_url = comment.link_id
    author = comment.author.name
    region = None
    subregion = None
    coven_name = None
    min_age = None
    current_timestamp = int(time.time())

    # Find the region
    for token in tokens:
        for region_name in regions:
            if token.lower() == region_name.lower():
                print(f"Found matching region: {region_name}")
                region = region_name
                break
        if region is not None:
            break

    if region is None:
        print("No matching region found. Send Modmail")
        return

    # Find the subregion
    for token in tokens:
        for subregion_name in subregions[region]:
            if token.lower() == subregion_name.lower():
                print(f"Found matching subregion: {subregion_name}")
                subregion = subregion_name
                break
        if subregion is not None:
            break

    if subregion is None:
        print("No matching subregion found. Send Modmail")
        return

    # Find the coven name
    for token in tokens:
        if token.startswith('"') and token.endswith('"'):
            print(f"Found coven name: {token}")
            coven_name = token.strip('"')
            break

    if coven_name is None:
        print("No matching coven name found. Send Modmail")
        return

    # Find the age requirement (optional)
    pattern = re.compile(r'^[0-9\-\+]+$')
    for token in tokens:
        if pattern.match(token):
            print(f"Found matching age token: {token}")
            min_age = token
            break


    print(f"Region: {region}, Subregion: {subregion}, Coven Name: {coven_name}, Min Age: {min_age}, Post URL: {post_url}, Timestamp: {current_timestamp}")
    record = (post_url, author, coven_name, region, subregion, min_age, current_timestamp)
    insert_irl_record(record)
    build_irl_wiki()

def parse_online(comment):
    print("Parsing Online comment (Not implemented)")
    # TODO


def send_modmail():
    print("Sending modmail")
    # TODO