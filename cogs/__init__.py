from . import facts, fluffy_bunnies, interact, jukebox, management, draw, misc, shitposting


def setup(bot):
    bot.add_cog(facts.Facts(bot))
    bot.add_cog(management.Manage())
    bot.add_cog(jukebox.Jukebox())
    bot.add_cog(interact.Interact())
    bot.add_cog(draw.Draw())
    bot.add_cog(misc.Misc())
    bot.add_cog(fluffy_bunnies.SoulPact())
    bot.add_cog(shitposting.ShitPosting())
