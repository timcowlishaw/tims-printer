from mastodon import Mastodon
import os
import time
from io import StringIO
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        super().__init__()
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.text = StringIO()
    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

#   Set up Mastodon
mastodon = Mastodon(
    access_token = os.environ.get("MASTODON_ACCESS_TOKEN"),
    api_base_url = os.environ.get("MASTODON_API_BASE_URL")
)
while True:
    time.sleep(10)
    for notification in mastodon.notifications(types=["mention"]):
        status = notification["status"]
        print("%s sent you this message at %s:" % (status["account"]["acct"], status["created_at"]))
        print(strip_tags(status["content"]))
        replied_to_id = status["in_reply_to_id"]
        if replied_to_id:
            replied_to = mastodon.status(replied_to_id)
            print("In reply to this toot from %s:" % replied_to["account"]["acct"])
            print(replied_to["url"])
            print(strip_tags(replied_to["content"]))
        print("--------------")
        mastodon.notifications_dismiss(notification["id"])