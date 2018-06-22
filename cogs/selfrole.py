import discord
from discord.ext import commands


class Selfrole:
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    async def pc(self, ctx):
        await self.selfrole(ctx, 'PC')

    @commands.command()
    @commands.guild_only()
    async def xbox(self, ctx):
        await self.selfrole(ctx, 'Xbox')

    @commands.command()
    @commands.guild_only()
    async def playstation(self, ctx):
        await self.selfrole(ctx, 'Playstation')

    @commands.command()
    @commands.guild_only()
    async def agree(self, ctx):
        await self.selfrole(ctx, 'Verified')

    async def selfrole(self, ctx, role: str):
        author = ctx.author
        guild = ctx.guild
        role = discord.utils.get(guild.roles, name=role)

        if role is None:
            return

        if role in author.roles:
            try:
                await author.remove_roles(role)
            except discord.Forbidden:
                pass
        elif role:
            try:
                await author.add_roles(role)
            except discord.Forbidden:
                pass


def setup(bot):
    r = Selfrole(bot)
    bot.add_cog(r)
