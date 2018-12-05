#!/usr/bin/env python3.6
import discord
from discord.ext import commands
from config import token

startup_extensions = ['selfrole']

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned, pm_help=None, help_attrs=dict(hidden=True))

@bot.event
async def on_ready():
    print(f'{bot.user.name} online')

if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(f'cogs.{extension}')

        except Exception as e:
            exc = f'{type(e).__name__}: {e}'

            print(f'Failed to load extension {extension}\n{exc}')

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    author = message.author
    guild = message.guild

    if message.content.startswith('+'):
        role = message.content[1:]
        role = discord.utils.get(guild.roles, name=role)

        if role is None:
            return

        try:
            await author.add_roles(role)
            await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

        except discord.Forbidden:
            await message.channel.send("Insufficient permissions.")

    if message.content.startswith('-'):
        role = message.content[1:]
        role = discord.utils.get(guild.roles, name=role)

        if role is None:
            return

        try:
            await author.remove_roles(role)
            await message.add_reaction('\N{WHITE HEAVY CHECK MARK}')

        except discord.Forbidden:
            await message.channel.send("Insufficient permissions.")

    await bot.process_commands(message)


bot.run(token)
