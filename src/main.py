import praw
from global_vars import init
init()
global subreddit
from global_vars import mod_list, config, subreddit
from db import connect_db
from geography import build_geography
from comment_processing import process_comment


# initialize with appropriate values
client_id = config.get('General', 'client_id')
client_secret = config.get('General', 'client_secret')
username = config.get('General', 'username')
password = config.get('General', 'password')
user_agent = config.get('General', 'user_agent')
supervisory_subreddit = config.get('General', 'supervisory_subreddit')

print(f"Attempting to connect with the following:\nclient_id: {client_id}\n client_secret: {client_secret}\n username: {username}\n password: {password}\n user_agent: {user_agent}")

# creating an authorized reddit instance
reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     username=username,
                     password=password,
                     user_agent=user_agent)

print("Connected to Reddit API")

# to find the top most submission in the supervisory subreddit
subreddit = reddit.subreddit(supervisory_subreddit)

print("\nTest - Getting top submission in supervisory subreddit...")
# get the top most submission as a test that the API is working
for submission in subreddit.top(limit = 1):
    print(f"Success! Top post in {supervisory_subreddit} is '{submission.title}' with {submission.score} upvotes")


print("\nSearching for moderators in the subreddit...")

for moderator in subreddit.moderator():
    print(f"Found moderator: {moderator}")
    mod_list.append(moderator)

print(f"Found {len(mod_list)} moderators in the subreddit")

# Setup other files
connect_db()
build_geography()

# testing wiki page for future
irl_wiki_page = config.get('Wiki', 'irl_page')

wiki_page = subreddit.wiki[irl_wiki_page]
#print(f"Found wiki page: {wiki_page.content_html}")



print("\nListing for new comments")
for comment in subreddit.stream.comments():
    process_comment(comment)