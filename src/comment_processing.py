import shlex # parse string like shell line
import re # regular expressions
import time

from global_vars import mod_list, regions, subregions
from db import insert_irl_record
from wiki import build_irl_wiki

def process_comment(comment) -> bool:
    author = comment.author
    is_mod = author in mod_list
    start_with_exclamation = comment.body.startswith("!")
    print(f"\nComment found ({comment}): {comment.body[:100]}")
    print(f"Author: {comment.author}. Is Mod:{is_mod}. Exclamation: {start_with_exclamation}")
    if is_mod == False or start_with_exclamation == False:
        print("Comment does not meet criteria. Ignoring...")
        return False
    print("Comment meets criteria. Processing...")
    response = "Unknown reason."
    if comment.body.startswith("!irl"):
        response = parse_irl(comment)
    elif comment.body.startswith("!online"):
        parse_online(comment)
        response = "Online command not supported yet"
    else:
        print("Comment does not match any command. Sending Mod Mail...")
        send_modmail("Unknown command",
                     f"Hello,\n\nAn unknown command was found in a comment. Please check the comment and ensure it is a valid command.\n\nYour comment has been deleted.\n\nComment:\n{comment.body}\n\nAcceptable commands: !irl, !online")
        response = "Unknown command"
    print("Deleting comment")
    comment.mod.remove(mod_note = f"Coven Bot - {response}")
    return True


def parse_irl(comment):
    print("Parsing IRL comment")
    tokens = shlex.split(comment.body, posix=False)
    print(f"Tokens: {tokens}")
    if not tokens:
        print("No tokens found. Ignoring")
        return "No tokens found"
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
        send_modmail("IRL Group missing region",
                     f"Hello,\n\nAn IRL Group post is missing a region, or it could not be detected. Please check the comment and add the region.\n\nYour comment has been deleted.\n\nComment:\n{comment.body}\n\nAcceptable Regions: {regions}")
        return "No region found"

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
        send_modmail("IRL Group missing subregion",
                     f"Hello,\n\nAn IRL Group post is missing a subregion, or it could not be detected. Please check the comment and add the subregion.\n\nYour comment has been deleted.\n\nComment:\n{comment.body}\n\nAcceptable Subregions: {subregions[region]}")
        return "No subregion found"

    # Find the coven name
    for token in tokens:
        if token.startswith('"') and token.endswith('"'):
            print(f"Found coven name: {token}")
            coven_name = token.strip('"')
            break

    if coven_name is None:
        print("No matching coven name found. Send Modmail")
        send_modmail("IRL Group missing coven name",
                     f"Hello,\n\nAn IRL Group post is missing a coven name, or it could not be detected. Please check the comment and add the coven.\n\nYour comment has been deleted.\n\nComment:\n{comment.body}\n\nThe coven name must be surrounded by double quotes. Example: \"Coven Name\"")
        return "No coven name found"

    # Find the age requirement (optional)
    pattern = re.compile(r'^[0-9\-\+]+$')
    for token in tokens:
        if pattern.match(token):
            print(f"Found matching age token: {token}")
            min_age = token
            break


    print(f"Region: {region}, Author: {author} Subregion: {subregion}, Coven Name: {coven_name}, Min Age: {min_age}, Post URL: {post_url}, Timestamp: {current_timestamp}")
    record = (post_url, author, coven_name, region, subregion, min_age, current_timestamp)
    insert_success = insert_irl_record(record)
    if insert_success:
        print("Record inserted successfully")
        from global_vars import config
        subreddit = config.get('General', 'supervisory_subreddit')
        irl_page = config.get('Wiki', 'irl_page')
        send_modmail(f"Successfully added IRL Group '{coven_name}'",
                     f"Hello,\n\nAn IRL group has been successfully added to the list and the wiki page has been edited.\n\nYou can view the wiki page [here](https://www.reddit.com/r/{subreddit}/wiki/{irl_page}).\n\nYour comment: {comment.body}\n\nPost information:\nRegion: {region}\nSubregion: {subregion}\nCoven Name: {coven_name}\nMinimum Age: {min_age}\n")
        build_irl_wiki()
        return "Successfully added"
    else:
        send_modmail("Database connection error",
                     f"Hello,\n\nA database connection error occurred while trying to add an IRL group.\n\nThis is a bug, please report to the developer.")
        return "Failed to add to DB"

def parse_online(comment):
    print("Parsing Online comment (Not implemented)")
    # TODO


def send_modmail(modmail_header, modmail_string):
    from main import subreddit
    print("Sending modmail")
    subreddit.message(subject = f"Coven Bot - {modmail_header}", message = modmail_string)