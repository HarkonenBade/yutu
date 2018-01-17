import os

from . import extensions
from .bot import Yutu
import pytumblr

def main():
    client = Yutu()
    client.load_extension("cogs")

    if 'YUTU_DEBUG' in os.environ:
        client.db.bind(provider='sqlite', filename=':memory:')
        client.tumblr = None  # FIXME
    else:
        client.db.bind(provider='postgres',
                       user=os.environ['POSTGRES_DB_USER'],
                       password=os.environ['POSTGRES_DB_PASS'],
                       database=os.environ['POSTGRES_DB'],
                       host=os.environ['POSTGRES_HOST'])
        client.tumblr = pytumblr.TumblrRestClient(
            os.environ['TUMBLR_CONSUMER_KEY'],
            os.environ['TUMBLR_CONSUMER_SECRET'],
            os.environ['TUMBLR_OAUTH_TOKEN'],
            os.environ['TUMBLR_OAUTH_SECRET']
        )

    client.db.generate_mapping(create_tables=True)

    client.run(os.environ['DISCORD_TOKEN'])