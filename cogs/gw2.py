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
        out = []
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
                    have = guild_info['favor']
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

            txt = f"{upgrade_info['name']} - {pcomp}%\n"
            txt += "\n".join(elms)
            out.append(txt)

        pages = []
        acc = ""
        for i in out:
            if len(acc) + len(i) > 2046:
                pages.append(acc)
                acc = ""
            acc += "\n\n" + i

        for i, p in enumerate(pages):
            if i==0:
                await ctx.send(embed=discord.Embed(title="Guild Upgrade Progress", description=p))
            else:
                await ctx.send(embed=discord.Embed(description=p))
