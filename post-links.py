'''
Sopel module to post new Reddit posts from a specific subreddit to a given IRC channel.

Defaults:
    subreddit: /r/bikewrench
    IRC channel: #biciklo
'''

import sopel.module
import praw

def checkRedditPost(botName, subredditText):

    reddit = praw.Reddit(botName)
    subreddit = reddit.subreddit(subredditText)

    for submission in subreddit.new(limit=1):

        subredditName = submission.subreddit_name_prefixed
        submissionTitle = submission.title
        submissionURL = submission.url

    return(subredditName, submissionTitle, submissionURL)

def shouldPost(submissionURL):

    with open('lastPost.txt', 'r') as lastPost:

        for post in lastPost.readlines():

            if post != submissionURL:
                post = True

                with open('lastPost.txt', 'w') as lastPost:
                    lastPost.write(submissionURL)
            else:
                post = False

    post = True

    if post
    return(post)

def main():

    botName = 'becykBot'
    subredditText = 'bikewrench'

    subredditName, submissionTitle, submissionURL = checkRedditPost(botName, subredditText)

    post = shouldPost(submissionURL)

    return(post, subredditName, submissionTitle, submissionURL)

@sopel.module.interval(60)
def doAction(bot):

    channel = '#biciklo'

    post, subredditName, submissionTitle, submissionURL = main()

    if post == True:
        if channel in bot.channels:
            bot.msg(channel, 'New post in {}: {}. More info here: {}'.format(subredditName, submissionTitle, submissionURL))

    else:
        pass
