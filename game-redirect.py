import logging
import os
import sys
import discord
from discord.ext import commands

logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

client = commands.Bot(command_prefix="/", intents=discord.Intents.all(), case_insensitive=True, self_bot=True)

# Create a dictionary to store the game-to-channel mappings
game_to_channel = {}

# Define a command to add a new game-to-channel mapping
@client.command(name="add")
async def add_game_channel(ctx, game, channel):
    game_to_channel[game] = channel
    log.info(f"Playing {game} will make members move to {channel} now.")
    # Send a confirmation message to the user
    await ctx.send(f"Playing {game} will make members move to {channel} now.")

# Define a command to list all game-to-channel mappings
@client.command(name="list")
async def list_game_channels(ctx):
    game_list = list(game_to_channel.items())

    game_strings = []
    for game, channel in game_list:
        game_strings.append(str(game) + " | " + str(channel))
    log.info(f"Game | Channel\n----------------\n{' | '.join(game_strings)}")
    # Send a message to the user listing all of the game-to-channel mappings
    await ctx.send(f"Game | Channel\n----------------\n{' | '.join(game_strings)}")

# Define a command to remove a game-to-channel mapping
@client.command(name="remove")
async def remove_game_channel(ctx, game):
    # Check if the game exists
    if game in game_to_channel:
        # If the game exists, remove it from the dictionary
        del game_to_channel[game]
        log.info(f"Playing {game} will not redirect anymore")
        await ctx.send(f"Playing {game} will not redirect anymore")
    else:
        log.warn(f"Game {game} is not redirected yet.")
        # If the game does not exist, send a message to the user
        await ctx.send(f"Game {game} is not redirected yet.")

# Define a command to move a user to a channel when they launch a game
@client.event
async def on_voice_state_update(member, before, after):
    # Check if the user is joining a voice channel
    if after.channel is not None:
        log.debug(f"{member} is in a VC.")
        # Check if the user is launching a game
        if member.activity is not None and member.activity.type == discord.ActivityType.playing:
            log.debug(f"{member} is playing {member.activity.name}.")
            # Check if there is a game-to-channel mapping for the game
            if member.activity.name in game_to_channel:
                log.info(f"{member} moved to {game_to_channel[member.activity.name]}.")
                # If there is a game-to-channel mapping, move the user to the channel
                await member.move_to(game_to_channel[member.activity.name])

# Run the bot
token = os.environ.get("DISCORD_BOT_TOKEN")
if token is None:
    log.fatal("Bot token must be stored in environment variable DISCORD_BOT_TOKEN !")
client.run(token)
