import argparse
import configparser
import discord
import asyncio
import requests
from discord.ext import commands
from discord.utils import get

bot = commands.Bot(command_prefix='!', help_command=None)

@bot.event
async def on_ready():
    """Prints a startup message."""
    print(str(bot.user) + ' is online.')
    await bot.change_presence(activity=discord.Game(name='!whitelist {username}'))


@bot.command()
async def whitelist(ctx, minecraftUser):
    if ctx.message.channel.id != 718200381301194882:
        emb = discord.Embed(
            description ='Error: Please use this command in #bot-commands.',
            title='Error',
            color=0x9b59b6
            )
        emb.set_footer(text='If you need help joining the server, read #lobby.')
        await ctx.message.channel.send(embed=emb)
    else:
        playerRole = get(ctx.message.guild.roles, name='Player')
        whitelistMsg = await ctx.send('whitelist add {}'.format(minecraftUser))
        await ctx.message.author.add_roles(playerRole)
        await whitelistMsg.delete(delay=10)
        emb = discord.Embed(
            description ='{} has been added to the whitelist.'.format(minecraftUser),
            title='Whitelist',
            color=0x3300bd
        )
        emb.set_footer(text='If you need help joining the server, read #lobby.')
        await ctx.channel.send(embed=emb)

def try_config(config, heading, key):
    """Attempt to extract config[heading][key], with error handling.

    This function wraps config access with a try-catch to print out informative
    error messages and then exit."""
    try:
        section = config[heading]
    except KeyError:
        print("Missing config section [{}]".format(heading))
        sys.exit(1)

    try:
        value = section[key]
    except KeyError:
        print("Missing config key '{}' under section '[{}]'".format(
            key, heading))
        sys.exit(1)
    return value

if __name__ == "__main__":
    # Parse command-line arguments for the token and the config file path.
    # It uses a positional argument for the token and a flag -c/--config to
    # specify the path to the config file.
    parser = argparse.ArgumentParser()
    #parser.add_argument("token")
    parser.add_argument(
        "-c", "--config", help="Config file path", default="config.ini")
    args = parser.parse_args()

    # Parse the config file at the given path, erroring out if keys are missing
    # in the config.
    config = configparser.ConfigParser()
    config.read(args.config)
    try:
        TOKEN = try_config(config, "IDs", "Token")
    except KeyError:
        sys.exit(1)

    bot.run(TOKEN)
