from twython import Twython
import json

def auth():
    with open("access.json", 'r') as f:
        db = json.load(f)
    return Twython(db["API_Key"], db["API_Secret"], db["Access_Token"], db["Access_Token_Secret"])

def load():
    with open("queue.json", 'r') as f:
        queue = json.load(f)
    with open("info.json", 'r') as fi:
        info = json.load(fi)
    return queue, info

def dump(queue, info):
    with open("queue.json", 'w') as f:
        json.dump(queue, f)
    with open("info.json", 'w') as fi:
        json.dump(info, fi)

def respond(twitter, top_tweet):
    name = top_tweet["user"]["screen_name"]
    twitter.update_status(status="@%s Willikers!" %(name), in_reply_to_status_id=top_tweet["id"])


def main():
    twitter = auth()
    queue, info = load()
    tweets = twitter.search(q="wizard people", result_type="recent", since_id=info["sinceid"], count='100')
    info["sinceid"] = tweets["search_metadata"]["max_id"]
    to_add = [tweet for tweet in tweets["statuses"] if not tweet["retweeted"] and not tweet.has_key("retweeted_status")]
    to_add = [tweet for tweet in to_add if "wizard people" in tweet.lower() or
                                        if "#wizardpeople" in tweet.lower()]
    queue = queue + to_add
    if len(queue) > 0:
        respond(twitter, queue.pop())
    dump(queue, info)

#run on cron every minute
if __name__ == "__main__":
    main()
