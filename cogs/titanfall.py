import discord
import random
import json
from collections import OrderedDict
from discord.ext import commands


# Copyright (c) 2017 Cynotek
class Titanfall:
    """Titanfall 2 utilities"""

    def __init__(self, bot):
        self.bot = bot
        self.items = 'data/titanfall/items.json'

    @commands.group()
    async def gen(self, ctx):
        """Generator commands"""
        if ctx.invoked_subcommand is None:
            pass

    @gen.group()
    async def pilot(self, ctx, *, opt=None):
        """Generates random pilot loadout"""
        author = ctx.author
        loadouts = self.open_items()
        pilot = loadouts['pilot']

        if opt:
            p = [f'**{p}:** {random.choice(pilot[p])}' for p in pilot if p.lower() == opt.lower()]
            if not p:
                return
        else:
            p = [f'**{p}:** {random.choice(pilot[p])}' for p in pilot]

        p = '\n'.join(p)
        em = discord.Embed(title=f"{author.name}'s loadout", description=p, colour=ctx.guild.me.color)
        await ctx.send(embed=em)

    @gen.group()
    async def titan(self, ctx):
        """Generates random titan loadout"""

        author = ctx.author
        titan = '\n'.join(self.gen_titan())

        em = discord.Embed(title=f"{author.name}'s loadout", description=titan, colour=ctx.guild.me.color)
        await ctx.send(embed=em)

    def gen_titan(self):
        items = []
        loadouts = self.open_items()
        titan = loadouts['titan']
        for t in titan:
            if isinstance(titan[t], list):
                if t == "Titan":
                    spec_titan = random.choice(titan[t])
                    items.append(f'**{t}:** {spec_titan}')
                else:
                    kit = random.choice(titan[t])
                    items.append(f'**{t}:** {kit}')
            else:
                spec_kit = random.choice(dict(titan[t].items())[spec_titan])
                items.append(f'**{t}:** {spec_kit}')

        return items

    def open_items(self):
        with open(self.items, 'r') as f:
            loadouts = json.loads(f.read(), object_pairs_hook=OrderedDict)
        return loadouts


def setup(bot):
    """Adds the cog"""
    t = Titanfall(bot)
    bot.add_cog(t)
