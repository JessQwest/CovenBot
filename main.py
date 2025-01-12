import praw
import configparser

# Load config
config = configparser.ConfigParser()
config.read('config/config.ini')

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
modList = []

for moderator in subreddit.moderator():
    print(f"Found moderator: {moderator}")
    modList.append(moderator)

print(f"Found {len(modList)} moderators in the subreddit")


def process_comment(comment):
    author = comment.author
    is_mod = author in modList
    start_with_exclamation = comment.body.startswith("!")
    print(f"\nComment found ({comment}): {comment.body[:100]}")
    print(f"Author: {comment.author}. Is Mod:{is_mod}. Exclamation: {start_with_exclamation}")
    if is_mod == False or start_with_exclamation == False:
        print("Comment does not meet criteria. Ignoring...")
        return
    print("Comment meets criteria. Processing...")


print("\nListing for new comments")
for comment in subreddit.stream.comments():
    process_comment(comment)