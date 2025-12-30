import snscrape.modules.twitter as sntwitter

keywords = [
    "mahseer",
    "golden mahseer",
    "Tor putitora",
    "Tor tor",
    "mahseer fish",
    "Indian mahseer"
]

query = "(" + " OR ".join(keywords) + ") lang:en"

tweets = []
for tweet in sntwitter.TwitterSearchScraper(query).get_items():
    tweets.append({
        "date": tweet.date,
        "username": tweet.user.username,
        "content": tweet.content,
        "url": tweet.url
    })

print(f"Collected {len(tweets)} tweets")