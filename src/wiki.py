from db import fetch_records


def fetch_header(header_name):
    print("Fetching header")
    with open(f"data/{header_name}.md", "r") as file:
        return file.read()

# TODO
def build_irl_wiki():
    header_text = fetch_header("irl_header")
    fetch_records("irl_groups")
