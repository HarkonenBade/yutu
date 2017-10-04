import os

from . import extensions
from .bot import Yutu

def main():
    client = Yutu()
    client.load_extension("cogs")

    if 'YUTU_DEBUG' in os.environ:
        client.db.bind(provider='sqlite', filename=':memory:')
    else:
        client.db.bind(provider='postgres',
                       user=os.environ['POSTGRES_DB_USER'],
                       password=os.environ['POSTGRES_DB_PASS'],
                       database=os.environ['POSTGRES_DB'],
                       host=os.environ['POSTGRES_HOST'])

    client.db.generate_mapping(create_tables=True)

    client.run(os.environ['DISCORD_TOKEN'])