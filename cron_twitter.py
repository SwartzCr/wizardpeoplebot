from twython import Twython
import json
import random

def auth():
    with open("access.json", 'r') as f:
        db = json.load(f)
    return Twython(db["API_Key"], db["API_Secret"], db["Access_Token"], db["Access_Token_Secret"])

def load_text():
    with open("text.json", 'r') as f:
        out = json.load(f)
    return out

def pick_paragraph(text):
    return text[random.randint(0,len(text)-1)]

def get_tweet(paragraph, tweet_text):
    if len(paragraph) <= 140:
        return paragraph
    else:
        # find punctuation
        punc = [i for (i, x) in enumerate(paragraph) if x in ["!", ".", "?"]]
        if len(punc) < 1:
            return ""
        shuffled_punc =  punc[:] + [0]
        random.shuffle(shuffled_punc)
        for place in shuffled_punc:
            remains = [x for x in punc if x > place]
            for end in remains[::-1]:
                if end - place <= 260:
                    if place != 0:
                        return paragraph[place+1:end+1].strip()
                    else:
                        return paragraph[place:end+1]
        return ""

def do_thing():
    twitter = auth()
    # load text
    text = load_text()
    tweet_text = ""
    while tweet_text == "":
        paragraph = pick_paragraph(text)
        tweet_text = get_tweet(paragraph, tweet_text)
        tweets = []
        if len(tweet_text) > 140:
            tweet1 = tweet_text[:135][::-1].split(" ", 1)[1][::-1]
            x = len(tweet1)
            tweet1 = tweet1+" (1/2)"
            tweet2 = tweet_text[x+1:]+" (2/2)"
            tweets.append(tweet1)
            tweets.append(tweet2)
        else:
            tweets.append(tweet_text)
    # send tweet
    for tweet in tweets:
        twitter.update_status(status=tweet)


do_thing()
