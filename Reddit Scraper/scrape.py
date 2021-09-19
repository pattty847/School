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
names = ["dankmemes", "memes", "MemeEconomy", "crappyoffbrands", "4chan"]


def get_top_10(names):

    for every in names:

        subreddit = reddit.subreddit(every)

        # Loop through the top posts in the subreddit, limit 10 posts
        for submission in subreddit.top(limit=5):

            # Grab URL and the extension
            url = str(submission.url)
            if(url.endswith("png") or url.endswith("jpeg") or url.endswith("jpg")):
                extension = url[-4:]
                print(extension)

                # Store content of url in request
                response = requests.get(url)

                images_file = open(every + "-" + submission.id + extension, "wb")
                images_file.write(response.content)
                images_file.close()



if names != None:
    get_top_10(names)