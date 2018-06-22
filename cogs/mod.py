import discord
import asyncio
from discord.ext import commands


class Mod:
    """Moderator only commands"""

    def __init__(self, bot):
        self.bot = bot
        self.time_format = {'m': 60,
                            'h': 3600,
                            'd': 14400}

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member, *, reason=None):
        "Bans user specified"

        if user is None:
            return
        elif user == ctx.author:
            return

        try:
            await ctx.guild.ban(user, reason=reason)
        except discord.Forbidden:
            return
        else:
            await ctx.send(f'{user.mention} banned.')

    @commands.command()
    @commands.guild_only()
    @commands.has_permissions(ban_members=True)
    async def hackban(self, ctx, user: int, *, reason=None):
        "Bans user specified"

        if user == ctx.author.id:
            return

        try:
            user = await self.bot.get_user_info(user)
        except discord.NotFound:
            return

        try:
            await self.bot.http.ban(user.id, ctx.guild.id, reason=reason)
        except discord.Forbidden:
            return
        else:
            await ctx.send(f'{user.mention} banned.')

    @commands.command(enabled=False)
    @commands.has_permissions(ban_members=True)
    async def mute(self, ctx, user: discord.Member, time='24h', *, reason=None):
        "Mutes user by adding a role"
        if user is None:
            return

        mutedrole = discord.utils.get(ctx.guild.roles, name='Muted')
        if mutedrole is None:
            mutedrole = await ctx.guild.create_role(name='Muted')

        time_num = [num for num in time if num.isdigit()]  # Extract digits

        orig_time = ''
        for num in time_num:
            orig_time += str(num)
        orig_time = int(orig_time)

        for i in self.time_format.keys():
            if i in time:
                mute_time = self.time_format[i] * orig_time
                break
            else:
                mute_time = orig_time

        await user.add_roles(mutedrole, reason=reason)
        await ctx.send(f'{user.mention} muted for {time}.')
        await asyncio.sleep(mute_time)
        await user.remove_roles(mutedrole)


def setup(bot):
    m = Mod(bot)
    bot.add_cog(m)
