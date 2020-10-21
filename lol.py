import praw

reddit = praw.Reddit(client_id = "0KxXFz3MNhqqQg",
					 client_secret = "Pz-9kbsz3Uh8PpDGJ6I_51B19Lg",
					 username = "Samrid_",
					 password = "Despacito@*",
					 user_agent = "python_praw")

subreddit = reddit.subreddit("memes")

top = subreddit.top(limit=5)

for submission in top:
    print(submission.title)