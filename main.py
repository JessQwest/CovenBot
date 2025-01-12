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

# to find the top most submission in the supervisory subreddit
subreddit = reddit.subreddit(supervisory_subreddit)
for submission in subreddit.top(limit = 1):
    # displays the submission title
    print(submission.title)
    # displays the net upvotes of the submission
    print(submission.score)
    # displays the submission's ID
    print(submission.id)
    # displays the url of the submission
    print(submission.url)