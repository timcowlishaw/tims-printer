from mastodon import Mastodon
import os
import time
from io import StringIO
from html.parser import HTMLParser
from escpos.printer import Usb

printer = Usb(0x0416, 0x5011)

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
for notification in mastodon.notifications(types=["mention"]):
    status = notification["status"]
    printer.text("%s sent you this message at %s:\n" % (status["account"]["acct"], status["created_at"]))
    printer.text(strip_tags(status["content"])+"\n")
    replied_to_id = status["in_reply_to_id"]
    if replied_to_id:
        replied_to = mastodon.status(replied_to_id)
        printer.text("In reply to this toot from %s:\n" % replied_to["account"]["acct"])
        printer.text(replied_to["url"]+"\n")
        printer.text(strip_tags(replied_to["content"])+"\n")
    printer.text("--------------\n\n\n\n")
    mastodon.notifications_dismiss(notification["id"])
printer.close()
