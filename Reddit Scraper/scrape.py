import requests
import praw
# SECRET: 3uj8Z8fk9RAR3LF1PCWkRPmT6WS3Ww
# PERSONAL: ZUv7j7NllnoOvEFb_MkdOw.
# <platform>:<app ID>:<version string> (by u/<Reddit username>)

# This program will download the latest trending memes from a list of subreddits. 
# Ranking of memes: comment count, upvotes, 


# Reddit authenticator method
reddit = praw.Reddit(
    client_id="ZUv7j7NllnoOvEFb_MkdOw",
    client_secret="3uj8Z8fk9RAR3LF1PCWkRPmT6WS3Ww",
    user_agent="<windows>:<com>:<0.1> (by u/<pat184>)",
    username = "pat184", 
    password = "Apollo420"
)

# Subreddit to search for memes
subreddit = reddit.subreddit("meme")

# Loop through the top posts in the subreddit, limit 10 posts
for submission in subreddit.top(limit=10):

    # Grab URL and the extension
    url = str(submission.url)
    extension = url[-4:]
    print(extension)

    # Store content of url in request
    response = requests.get(url)

    file = open(submission.id + extension, "wb")
    file.write(response.content)
    file.close()