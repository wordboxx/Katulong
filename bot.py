# Imports
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.event_functions import *

# Print current working directory
print(f"Current working directory: {os.getcwd()}")

# Load variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set up the bot with proper intents
intents = discord.Intents.default()
intents.message_content = True  # Required for message content
bot = commands.Bot(command_prefix='!', intents=intents)
commands = [
    "ping",
    "events",
    "add_event"
]

# Bot events
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.command()
async def ping(ctx):
    """Test the bot's latency."""
    await ctx.send("Pong!")

@bot.command()
async def events(ctx):
    """Display all scheduled events."""
    await ctx.send(format_events(get_events()))

@bot.command()
async def add_event(ctx):
    """Add a new event."""
    await add_new_event(ctx, bot)

@bot.command()
async def delete_event(ctx):
    """Delete an event."""
    await remove_event(ctx, bot)

@bot.command()
async def countdown(ctx):
    """Display the time until all events."""
    events = get_events()
    await ctx.send("**Event Countdowns:**\n" + events_countdown(events))

# Run the bot
bot.run(TOKEN)