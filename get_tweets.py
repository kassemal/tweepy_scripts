#!/usr/bin/env python
# encoding: utf-8

"""
For every user in $USR_ID list, get the most recent $TWEETS_NB tweets 
and write them into a sperate file. 
"""
import tweepy #https://github.com/tweepy/tweepy

#Twitter API credentials 
consumer_KEY = []
consumer_SECRET = []
access_TOKEN = [] 
access_TOKEN_SECRET = []


def get_id_tweets(id_u, k):
    """
    Get last $k tweets of user $id_u.
    """
    tweets = [] 
    if k < 200:
        tweets = api.user_timeline(id_u, count=k)
        return tweets
    else:
        new_tweets = api.user_timeline(id_u, count=200)
        tweets.extend(new_tweets)
        last_twt_id = tweets[-1].id - 1
        k = k - len(new_tweets) #200
        while(len(new_tweets) == 200 and k > 200):      
            #getting tweets with id smaller than $last_twt_id
            new_tweets = api.user_timeline(id_u, count=200, max_id=last_twt_id)
            tweets.extend(new_tweets)
            last_twt_id = tweets[-1].id - 1
            k = k - len(new_tweets) #200
        if len(new_tweets) == 200:
            new_tweets = api.user_timeline(id_u, count=k, max_id=last_twt_id)
            print(api.auth_idx)
            tweets.extend(new_tweets)
        return tweets
        
USR_ID = ['CHANEL', 'FIFAWorldCup'] #list of screen_name (str) or id (int)
TWEETS_NB = 500

if __name__ == '__main__':

    #authentication
    # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    # auth.set_access_token(access_token, access_token_secret)
    # api = tweepy.API(auth, wait_on_rate_limit=True)
    auth_list = []
    for i in range(len(consumer_KEY)):
        auth_i = tweepy.OAuthHandler(consumer_KEY[i], consumer_SECRET[i])
        auth_i.set_access_token(access_TOKEN[i], access_TOKEN_SECRET[i])
        auth_list.append(auth_i)
    api = tweepy.API(auth_list, monitor_rate_limit=True, wait_on_rate_limit=True)

    for i, id_u in enumerate(USR_ID):
        #get tweets of user $id_u
        print('Getting tweets of user %d ...'%(i+1))
        tweets = get_id_tweets(id_u, TWEETS_NB) 

        #obtain the id in case if that the username is provided
        if isinstance(id_u, str):
            id_u = api.get_user(id_u).id

        #write tweets into a file
        if i == 0:
            mode = 'wb'
        else:
            mode = 'a'
        f = open("tweets_log", mode)
        for twt in tweets:
            formated_twt = [id_u, twt.id_str, twt.created_at, twt.text.encode("utf-8").replace('\n', ' ')]
            if twt.is_quote_status:
                try:
                    formated_twt.append(twt.quoted_status_id_str)
                except AttributeError:
                    formated_twt.append('None')
            else:
                try:
                    formated_twt.append(twt.retweeted_status.id_str)
                except AttributeError:
                    formated_twt.append(twt.in_reply_to_status_id_str)
            f.write(';'.join(str(x) for x in formated_twt) + '\n')
        f.close()
    print('Done!')


