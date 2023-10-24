# from https://shkspr.mobi/blog/2018/08/easy-guide-to-building-mastodon-bots/
from mastodon import Mastodon
import os

#   Set up Mastodon
mastodon = Mastodon(
    access_token = os.environ.get("MASTODON_ACCESS_TOKEN"),
    api_base_url = os.environ.get("MASTODON_API_BASE_URL")
)

mastodon.status_post("hello world with env var!")