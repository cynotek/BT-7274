import discord
from discord.ext import commands
from config.config import cogs_dir
from sys import version_info


class Admin:
    """Bot administrator only commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.is_owner()
    async def guilds(self, ctx):
        "Lists guilds"
        if ctx.invoked_subcommand is None:

            guilds = enumerate([guild for guild in self.bot.guilds], 1)
            guilds = [f'{num}. {g.name}' for num, g in guilds]
            guilds = '\n'.join(guilds)

            em = discord.Embed(title='Guilds', description=guilds, colour=ctx.guild.me.color)
            await ctx.send(embed=em)

    @guilds.command()
    async def leave(self, ctx, guild_num: int):
        "Leave a guild by typing it's number"
        guilds = enumerate([guild for guild in self.bot.guilds], 1)
        for num, guild in guilds:
            if num == guild_num:
                await ctx.send(f'Left {guild.name}.')
                await guild.leave()

    @commands.group(name='cogs')
    @commands.is_owner()
    async def _cog(self, ctx):
        if ctx.invoked_subcommand is None:
            cogs = '\n'.join(self.bot.cogs.keys())
            em = discord.Embed(title='Cogs', description=cogs, colour=ctx.guild.me.color)
            await ctx.send(embed=em)

    @_cog.command()
    async def load(self, ctx, *, module: str):
        """Loads a module."""
        try:
            self.bot.load_extension(f'{cogs_dir}{module}')
        except Exception as e:
            await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send(f'{module} loaded.')

    @_cog.command()
    async def unload(self, ctx, *, module: str):
        """Unloads a module."""
        try:
            self.bot.unload_extension(f'{cogs_dir}{module}')
        except Exception as e:
            await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send(f'{module} unloaded.')

    @_cog.command()
    async def reload(self, ctx, *, module: str):
        """Reloads a module."""
        try:
            self.bot.unload_extension(f'{cogs_dir}{module}')
            self.bot.load_extension(f'{cogs_dir}{module}')
        except Exception as e:
            await ctx.send(f'{type(e).__name__}: {e}')
        else:
            await ctx.send(f'{module} reloaded.')

    @commands.command()
    @commands.is_owner()
    async def shutdown(self):
        "Shuts down bot"
        await self.bot.logout()

    @commands.command()
    @commands.is_owner()
    async def version(self, ctx):
        "Displays version"
        dpy = discord.__version__

        py = version_info[:3]
        py = f'{py[0]}.{py[1]}.{py[2]}'

        desc = f"**Discord.py: **{dpy}\n**Python: **{py}"
        em = discord.Embed(description=desc, colour=ctx.guild.me.color)
        await ctx.send(embed=em)


def setup(bot):
    a = Admin(bot)
    bot.add_cog(a)
