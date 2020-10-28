# Ihihi-Bot

This bot is a Simple yet Advanced bot to be used for custom servers. I made this so that I can use it with my friends in my server, but as it has many features; I have made the repo public so that you are able to use it. :)

## How to use the bot (Locally)?
**I AM EXPECTING ANYONE USING THIS CODE TO HAVE A DISCORD BOT TOKEN *(OR ATLEAST KNOW HOW TO MAKE A BOT AND GET ITS TOKEN)* AND A BASIC PYTHON KNOWLEDGE!**
1. Clone this repo in your local machine.
2. Enable your Virtual Environment. (Optional)
3. Run this command `pip install -r requirements.txt` 
4. Goto https://www.reddit.com/prefs/apps and make a new app *(Script)*.
5. Goto https://cloud.mongodb.com/ and make a cluster which can be accessed from any ip, also make a account which can be used to access the cluster!
6. Click on connect and select python driver, then select python 3.6.
7. Now goto your directory of the bot and create a `.env` file.
8. Now paste the value that you obtained from mongodb and python praw as given in the image and the code below:

``PASSWORD=<YOUR REDDIT PASSWORD>
USERNAME=<YOUR REDDIT USERNAME>
TOKEN=<YOUR BOT TOKEN>
MONGOCLIENT=<YOUR LINK YOU GOT FROM MONGODB>
SECRET=<YOUR PRAW SECRET>
ID=<YOUR PRAW APP ID>``

![Add the variables you have in this format](https://i.ibb.co/rxwvNjx/env.png)

9. Replace the `<dbname>` in your mongodb link with `test` and replace username and password *(Should be url encoded)* with your account values.
10. Now goto your discord developer portal and enable intents in your bot. *(If you don't know how to do; FUCKING GOOGLE IT DUMBASS)*
11. Now goto your local directory and run the bot.py.

*(If you get any errors, add the problem in issues.)*

## How to host the bot on heroku?
1. Do every step how to host the bot locally.
2. Goto heroku and make one app.
3. Goto the settings page and then add python build pack.
4. Also add the key, value pairs you used in `.env` in config vars of heroku.
5. Upload your directory to github.
6. Goto deploy page in heroku, then click github, and select the repo where you have uploaded the bot.
7. Now deploy it.
*(If you get any errors, add the problem in issues.)*

Credits: Samrid Pandit
**Feel free to modify the bot and submit pull requests :)**
