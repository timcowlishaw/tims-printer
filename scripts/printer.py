from mastodon import Mastodon
import os
from unidecode import unidecode
import emoji
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

    def handle_endtag(self, tag):
        if tag in ["br", "p"]:
            self.text.write("\n\n")

    def handle_data(self, d):
        self.text.write(d)
    def get_data(self):
        return self.text.getvalue()

def asciify(html):
    s = MLStripper()
    s.feed(html)
    return unidecode(emoji.demojize(s.get_data()))

#   Set up Mastodon
mastodon = Mastodon(
    access_token = os.environ.get("MASTODON_ACCESS_TOKEN"),
    api_base_url = os.environ.get("MASTODON_API_BASE_URL")
)
for notification in mastodon.notifications(types=["mention"]):
    status = notification["status"]
    printer.text("%s sent you this message at %s:\n\n" % (status["account"]["acct"], status["created_at"]))
    printer.text(asciify(status["content"])+"\n\n")
    replied_to_id = status["in_reply_to_id"]
    if replied_to_id:
        replied_to = mastodon.status(replied_to_id)
        printer.text("In reply to this toot from %s:\n\n" % replied_to["account"]["acct"])
        printer.text(replied_to["url"]+"\n\n")
        printer.text(asciify(replied_to["content"])+"\n\n")
    printer.text("--------------\n\n\n\n")
    mastodon.notifications_dismiss(notification["id"])
printer.close()
