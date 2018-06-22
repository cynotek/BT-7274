from discord.ext import commands
from discord import Permissions, utils, Member, Embed, HTTPException


class General:
    """General commands"""

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def oauth(self, ctx):
        """Sends bot oauth url"""
        url = utils.oauth_url(self.bot.user.id, permissions=Permissions(8))

        await ctx.author.send(url)

    @commands.command()
    @commands.guild_only()
    async def userinfo(self, ctx, *, user: Member=None):
        """Shows users's information"""
        author = ctx.author
        server = ctx.guild

        if not user:
            user = author

        roles = [x.name for x in user.roles if x.name != "@everyone"]

        joined_at = user.joined_at
        since_created = (ctx.message.created_at - user.created_at).days
        since_joined = (ctx.message.created_at - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y %H:%M")
        user_created = user.created_at.strftime("%d %b %Y %H:%M")
        member_number = sorted(server.members,
                               key=lambda m: m.joined_at).index(user) + 1

        created_on = "{}\n({} days ago)".format(user_created, since_created)
        joined_on = "{}\n({} days ago)".format(user_joined, since_joined)

        game = "Chilling in {} status".format(user.status)

        if user.game is None:
            pass
        elif user.game.url is None:
            game = "Playing {}".format(user.game)
        else:
            game = "Streaming: [{}]({})".format(user.game, user.game.url)

        if roles:
            roles = sorted(roles, key=[x.name for x in server.role_hierarchy
                                       if x.name != "@everyone"].index)
            roles = ", ".join(roles)
        else:
            roles = "None"

        data = Embed(description=game, colour=user.color)
        data.add_field(name="Joined Discord on", value=created_on)
        data.add_field(name="Joined this server on", value=joined_on)
        data.add_field(name="Roles", value=roles, inline=False)
        data.set_footer(text=f"Member #{member_number} | User ID:{user.id}")

        name = str(user)
        name = " ~ ".join((name, user.nick)) if user.nick else name

        if user.avatar_url:
            data.set_author(name=name, url=user.avatar_url)
            data.set_thumbnail(url=user.avatar_url)
        else:
            data.set_author(name=name)

        try:
            await ctx.send(embed=data)
        except HTTPException:
            await ctx.send("I need the `Embed links` permission "
                           "to send this")

    @commands.command(hidden=True)
    async def ping(self, ctx):
        """Pong."""
        await ctx.send('Pong.')


def setup(bot):
    g = General(bot)
    bot.add_cog(g)
