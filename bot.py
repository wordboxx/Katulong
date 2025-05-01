# Imports
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.event_functions import (
    add_new_event,
    remove_event,
    format_events,
    events_countdown,
    get_events,
)

# Print current working directory
print(f"Current working directory: {os.getcwd()}")

# Load variables from .env file
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")
if TOKEN is None:
    raise ValueError("TOKEN is not set in environment variables.")

# Set up the bot with proper intents
intents = discord.Intents.default()
intents.message_content = True  # Required for message content
bot = commands.Bot(command_prefix="!", intents=intents)


# Bot events
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(e)


@bot.tree.command(name="ping", description="Test the bot's latency.")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("Pong!")


@bot.tree.command(name="events", description="Display all scheduled events.")
async def events(interaction: discord.Interaction):
    await interaction.response.send_message(format_events(get_events()))


@bot.tree.command(name="add_event", description="Add a new event.")
async def add_event(interaction: discord.Interaction):
    await add_new_event(interaction, bot)


@bot.tree.command(name="delete_event", description="Delete an event.")
async def delete_event(interaction: discord.Interaction):
    await remove_event(interaction, bot)


@bot.tree.command(name="countdown", description="Display the time until all events.")
async def countdown(interaction: discord.Interaction):
    events = get_events()
    await interaction.response.send_message(
        "**Event Countdowns:**\n" + events_countdown(events)
    )


# Run the bot
bot.run(TOKEN)
