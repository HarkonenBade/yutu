import os

import discord
from discord.ext import commands

import gw2api

class GW2(commands.Cog):
    def __init__(self):
        self.gw2 = gw2api.GuildWars2Client(api_key=os.environ['GW2API'])
        self.velv = os.environ['GW2GUILDID']

    @commands.command()
    async def gw2hall(self, ctx: commands.Context):
        out = "Guild Upgrade Progress\n"
        treasury = self.gw2.guildidtreasury.get(id=self.velv)
        active_upgrades = {v['upgrade_id'] for i in treasury for v in i['needed_by']}
        treasury = {v['item_id']: v for v in treasury}
        guild_info = self.gw2.guildid.get(id=self.velv)

        for i in active_upgrades:
            completion = 0
            elms = []
            upgrade_info = self.gw2.guildupgrades.get(id=i)

            for cost in upgrade_info['costs']:
                needed = cost['count']
                if cost['name'] == "Guild Favor":
                    have = guild_info['favour']
                elif cost['name'] == "Aetherium":
                    have = guild_info['aetherium']
                else:
                    have = treasury[cost['item_id']]['count']

                if have >= needed:
                    completion += 1
                    elms.append(f"    ~~{needed}/{needed} {cost['name']}~~")
                else:
                    elms.append(f"    {have}/{needed} {cost['name']}")

            pcomp = completion * 100 // len(upgrade_info['costs'])

            out += f"{upgrade_info['name']} - {pcomp}\n"
            out += "\n".join(elms)
            out += "\n\n"

        await ctx.send(embed=discord.Embed(description=out))
