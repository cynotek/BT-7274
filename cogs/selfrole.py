import discord
from discord.ext import commands


class Selfrole:
    def __init__(self, bot):
        self.bot = bot


    @commands.group()
    async def roles(self, ctx):
        """Generator commands"""
        if ctx.invoked_subcommand is None:
            guild = ctx.guild
            roles = enumerate([role for role in guild.roles], 1)
            roles = [f'{num}. {r.name}' for num, r in roles]
            roles = '\n'.join(roles)

            em = discord.Embed(title=f"{guild.name}'s roles", description=roles, colour=ctx.guild.me.color)
            await ctx.send(embed=em)


def setup(bot):
    r = Selfrole(bot)
    bot.add_cog(r)
