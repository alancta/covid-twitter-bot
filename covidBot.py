#!/usr/bin/env python3

import tweepy
import time
import requests

print("Initializing COVID-19 TWITTER BOT - Created by Alan Chuan")

CONSUMER_KEY = 'xxxxx'
CONSUMER_SECRET = 'xxxxx'
ACCESS_KEY = 'xxxxx'
ACCESS_SECRET = 'xxxxx'
FILE_NAME = 'last_seen_id.txt'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
mentions = api.mentions_timeline()
link = "https://covid-19-coronavirus-statistics.p.rapidapi.com/v1/total"

def retrieve_last_seen_id(file_name):
    """Retrieve the ID of the last seen tweet"""
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


def store_last_seen_id(last_seen_id, file_name):
    """Store the ID of the last seen tweet"""
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return

def reply_to_tweets():
    """Reply to tweets"""
    print('retrieving and replying to tweets...')
    last_seen_id = retrieve_last_seen_id(FILE_NAME)
    # NOTE: We need to use tweet_mode='extended' below to show
    # all full tweets (with full_text). Without it, long tweets
    # would be cut off.
    mentions = api.mentions_timeline(
        last_seen_id,
        tweet_mode='extended')

    # reverse the list because we want to retrieve the mentions
    # in chronological order
    for mention in reversed(mentions):
        print(str(mention.id) + ' - ' + mention.full_text)
        last_seen_id = mention.id
        list = mention.full_text.lower().split()
        country_name = list[1].lower().capitalize()
        # stores the last seen tweet/last tweet that the bot replied to
        store_last_seen_id(last_seen_id, FILE_NAME)
        if '#status' in mention.full_text.lower():
            print('found #status!')
            print('responding...')

            # COVID BOT START#
            url = link
            host = "covid-19-coronavirus-statistics.p.rapidapi.com"
            key = "bccf3719d1msh6c99e7e0c2b38e2p154225jsnf19a47572a99"

            querystring = {"country": country_name}

            headers = {
                'x-rapidapi-host': host,
                'x-rapidapi-key': key
            }

            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            data = response.json()
            data = data['data']

            country = data['location']
                        if country != "Global":
                confirmed = str(data['confirmed'])
                deaths = str(data['deaths'])
                recovered = str(data['recovered'])
                # COVID BOT END#
                # Tweet at the original tweeter
                api.update_status('@' + mention.user.screen_name
                                  + "\nCountry: " + country + "\n" + "Confirmed: "
                                  + confirmed + "\n" + "Deaths: " + deaths + "\n"
                                  + "Recovered: " + recovered, mention.id)

if __name__ == '__main__':
    reply_to_tweets()
