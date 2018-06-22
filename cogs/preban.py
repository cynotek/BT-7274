import discord
from discord.ext import commands
from asyncio import InvalidStateError
import json


# Copyright (c) 2017 Cynotek
class Preban:
    """Global user blacklist module"""

    def __init__(self, bot):
        self.bot = bot
        self.banlist = "data/preban/banlist.json"
        self.lbans = bot.loop.create_task(self.openlocal())

    @commands.group()
    @commands.is_owner()
    async def p(self, ctx):
        """Preban commands"""
        if ctx.invoked_subcommand is None:
            pass

    @p.group(name="list")
    async def _list(self, ctx):
        """Lists blacklisted users."""
        try:
            lbans = self.lbans.result()
        except InvalidStateError:
            return

        blist = [usr.mention for usr in lbans]
        blist = '\n'.join(blist)

        await ctx.author.send(blist)

    @p.group()
    async def update(self, ctx):
        """Preemptivly bans all users in the ban list."""
        await ctx.send("Updating ban definitions...")
        guilds = self.bot.guilds

        [await self.preban(guild) for guild in guilds]

        await ctx.send(f"Ban definitions updated in {len(guilds)} guilds.")

    async def on_guild_join(self, guild):
        """Preemptively ban all accounts in the list on bot join if possible"""
        await self.preban(guild)

    async def preban(self, guild):
        """Pass in the local bans, then generate the current guild bans"""
        try:
            lbans = self.lbans.result()
        except InvalidStateError:
            return

        BanEntry = await guild.bans()
        sbans = [user for reason, user in BanEntry]  # Discards reasons and appends server bans
        targets = [user for user in lbans if user not in sbans]  # Avoid banning users who are already banned

        if targets:
            for user in targets:
                try:
                    await self.bot.http.ban(user.id, guild.id, reason='Preemptive')
                except discord.Forbidden:
                    pass

    async def openlocal(self):
        """Parse the local ban list of ids into user objects"""
        await self.bot.wait_until_ready()

        with open(self.banlist, 'r') as blist:
            rawids = json.loads(blist.read())

        lbans = []
        for i in rawids:
            try:
                usr = await self.bot.get_user_info(i)
            except discord.NotFound:
                pass
            else:
                lbans.append(usr)

        return lbans


def setup(bot):
    """Adds the cog"""
    p = Preban(bot)
    bot.add_cog(p)
