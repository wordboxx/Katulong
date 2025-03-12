# Imports
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from utils import event_functions

if __name__ == "__main__":
    print("Starting bot...")

# Load environment variables.
try:
    load_dotenv(dotenv_path='data/.env')
except:
    print(f"Something went wrong loading from data directory!")
    exit(1)

# Setup intents.
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

# Create bot instance with intents.
bot = commands.Bot(command_prefix='!', intents=intents)

# Bot Functions
# --- Logged in.
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}!')

# --- If the bot is mentioned in message.
@bot.event
async def on_message(message):
    # Don't respond to our own messages.
    if message.author == bot.user:
        return

    # Check if the bot was mentioned in the message.
    if bot.user.mentioned_in(message):
        # TODO: Fill out command list when pinged.
        await message.channel.send(event_functions.help())

    # This line is important! It processes commands.
    await bot.process_commands(message)

# Commands (like !ping)
# --- !ping: test to see if bot is working.
@bot.command()
async def ping(ctx):
    await ctx.send('Pong!')

# --- !events: lists help menu for all events functions.
@bot.command()
async def events(ctx):
    await event_functions.events(ctx)

# --- !list_events: lists all events in events.json.
@bot.command()
async def list_events(ctx):
    await event_functions.list_events(ctx)

# --- !add_event: add an event to events.json
@bot.command()
async def add_event(ctx):
    await event_functions.add_event(ctx)

# --- !remove_event: removes an event from events.json
@bot.command()
async def remove_event(ctx):
    await event_functions.remove_event(ctx)

# Get token from environment variable.
TOKEN = os.getenv('DISCORD_TOKEN')
if not TOKEN:
    raise ValueError("No token found. Make sure DISCORD_TOKEN is set in .env file")

bot.run(TOKEN)