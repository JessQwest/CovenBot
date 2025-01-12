from db import fetch_records
from src.data_class.IRLGroup import IRLGroup
from global_vars import archive_md, subreddit

def fetch_header(header_name):
    print("Fetching header")
    with open(f"data/{header_name}.md", "r") as file:
        return file.read()


def build_irl_wiki():
    print("\n\n\n\n\nSUBREDDIT:", subreddit)
    final_markdown = fetch_header("irl_header") + "\n" + archive_md + "\n\n"
    irl_records_raw = fetch_records("irl_groups")
    irl_records = [IRLGroup(*row) for row in irl_records_raw]
    print("Building IRL wiki")

    # Step 1: Create a dictionary to group records by region and subregion
    grouped_records = {}

    # Step 2: Populate the dictionary
    for record in irl_records:
        region = record.region
        subregion = record.subregion
        if region not in grouped_records:
            grouped_records[region] = {}
        if subregion not in grouped_records[region]:
            grouped_records[region][subregion] = []
        grouped_records[region][subregion].append(record)

    # Step 3: Convert the dictionary to a sorted list of tuples
    sorted_grouped_records = sorted(
        [(region, sorted(subregions.items())) for region, subregions in grouped_records.items()]
    )

    # Step 4: Format the list into markdown
    for region, subregions in sorted_grouped_records:
        final_markdown += f"#{region}\n---\n\n"
        for subregion, records in subregions:
            final_markdown += f"{subregion}\n\n"
            for record in records:
                min_age_text = ""
                if record.min_age is not None:
                    min_age_text = f" ({record.min_age})"
                final_markdown += f"* [{record.coven_name}](https://www.reddit.com/r/{subreddit}/comments/{record.post_url}){min_age_text} by u/{record.author}\n"

    print("Final markdown:", final_markdown)
    print("Wiki built")