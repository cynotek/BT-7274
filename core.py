#!/usr/bin/env python3.6
import asyncio
from discord.ext import commands
from config import token
import traceback
import sys

try:
    import uvloop
except ImportError:
    pass
else:
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

desc = """
       BT-7274 - built by Cynotek
       """

startup_extensions = ['general',
                      'selfrole']

bot = commands.AutoShardedBot(command_prefix=commands.when_mentioned_or('!'), description=desc, pm_help=None, help_attrs=dict(hidden=True))


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send('This command cannot be used in private messages.')
    elif isinstance(error, commands.DisabledCommand):
        await ctx.author.send('Sorry. This command is disabled and cannot be used.')
    elif isinstance(error, commands.CommandInvokeError):
        print(f'In {ctx.command.qualified_name}:', file=sys.stderr)
        traceback.print_tb(error.original.__traceback__)
        print(f'{error.original.__class__.__name__}: {error.original}', file=sys.stderr)


if __name__ == "__main__":
    for extension in startup_extensions:
        try:
            bot.load_extension(f'cogs.{extension}')
        except Exception as e:
            exc = f'{type(e).__name__}: {e}'
            print(f'Failed to load extension {extension}\n{exc}')

    bot.run(token)
