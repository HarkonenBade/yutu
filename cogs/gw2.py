import json
import os

import discord
from discord.ext import commands

import gw2api

class GW2(commands.Cog):
    def __init__(self):
        self.gw2 = gw2api.GuildWars2Client(api_key=os.environ['GW2API'])
        self.velv = os.environ['GW2GUILDID']
        with open("data/upgrades.json") as f:
            self.upgrades = json.load(f)

    @commands.command()
    async def gw2hall(self, ctx: commands.Context):
        categories = {"General": [],
                      "Tavern": [],
                      "Mine": [],
                      "Workshop": [],
                      "Arena": [],
                      "Market": [],
                      "War Room": []}

        treasury = self.gw2.guildidtreasury.get(id=self.velv)
        guild_upgrades = set(self.gw2.guildidupgrades.get(id=self.velv))
        active_upgrades = {v['upgrade_id'] for i in treasury for v in i['needed_by'] if set(self.upgrades[v['upgrade_id']]['prerequisites']) <= guild_upgrades}
        treasury = {v['item_id']: v for v in treasury}
        guild_info = self.gw2.guildid.get(id=self.velv)

        for cat in categories:
            cur_upgrades = [self.upgrades[v] for v in active_upgrades if self.upgrades[v]['location'] == cat]
            for upgrade in cur_upgrades:
                completion = 0
                elms = []
                for cost in upgrade['costs']:
                    needed = cost['count']
                    if cost['type'] == "Coins":
                        have = 0
                    elif cost['name'] == "Guild Favor":
                        have = guild_info['favor']
                    elif cost['name'] == "Aetherium":
                        have = guild_info['aetherium']
                    else:
                        have = treasury[cost['item_id']]['count']

                    if have >= needed:
                        completion += 1
                        elms.append(f"~~{needed}/{needed} {cost['name']}~~")
                    else:
                        elms.append(f"{have}/{needed} {cost['name']}")

                pcomp = completion * 100 // len(upgrade['costs'])

                txt = f"**{upgrade['name']}** - {pcomp}%\n"
                txt += "\n".join(elms)
                categories[cat].append(txt)

        out = discord.Embed(title = "Guild Upgrade Progress")

        for cat in categories:
            ups = categories[cat]
            if len(ups) == 0:
                continue

            title = ""
            if cat == "General":
                title = "🧰 General"
            elif cat == "Tavern":
                title = "🍺 Tavern"
            elif cat == "Mine":
                title = "⛏️ Mine"
            elif cat == "Workshop":
                title = "🛠 Workshop"
            elif cat == "Arena":
                title = "⚔️ Arena"
            elif cat == "Market":
                title = "⚖️ Market"
            elif cat == "War Room":
                title = "🛡 War Room"
            out.add_field(title, "\n\n".join(ups))

        await ctx.send(embed=out)
