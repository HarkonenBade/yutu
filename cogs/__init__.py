from . import (facts, fluffy_bunnies, interact,
               jukebox, management, draw,
               misc, shitposting, self_management,
               kali, games, custom, gw2)

def setup(bot):
    bot.add_cog(facts.Facts(bot))
    bot.add_cog(games.Games(bot))
    bot.add_cog(custom.CustomCommands(bot))
    bot.add_cog(management.Manage())
    bot.add_cog(jukebox.Jukebox())
    bot.add_cog(interact.Interact())
    bot.add_cog(draw.Draw())
    bot.add_cog(misc.Misc())
    bot.add_cog(fluffy_bunnies.SoulPact())
    bot.add_cog(shitposting.ShitPosting())
    bot.add_cog(self_management.selfmanagement())
    bot.add_cog(kali.KaliCommands())
    bot.add_cog(gw2.GW2())
