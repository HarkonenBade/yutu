import os
import discord
from discord.ext.commands import Bot, when_mentioned_or

from pony import orm

DESCRIPTION = """
Hi, I'm Yutu!
I'm the bot for the Velvet fan discord.
I'm still learning so sorry if I do something wrong.
You can ask my programmer @Harkonen if you want to know more about me.
"""

client = Bot(when_mentioned_or("~"),
             game=discord.Game(name="~help"),
             description=DESCRIPTION)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    client.owner_id = (await client.application_info()).owner.id

client.db = orm.Database()

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
