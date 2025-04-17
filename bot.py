# Imports
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv
from utils.event_functions import get_events, add_new_event, format_events, date_checker

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
    await ctx.send("Pong!")

@bot.command()
async def help(ctx):
    await ctx.send(f"Available commands: {', '.join(commands)}")

@bot.command()
async def events(ctx):
    """Display all scheduled events."""
    await ctx.send(format_events(get_events()))

@bot.command()
async def add_event(ctx):
    """Add a new event."""
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    try:
        await ctx.send("Enter the event name:")
        name_msg = await bot.wait_for('message', check=check, timeout=30.0)
        
        await ctx.send("Enter the event date (MM/DD/YYYY only):")
        date_msg = await bot.wait_for('message', check=check, timeout=30.0)
        
        if not date_checker(date_msg.content):
            await ctx.send("Invalid date format or date is in the past. Please use MM/DD/YYYY.")
            return
        
        await add_new_event(ctx, name_msg.content, date_msg.content)
        await ctx.send(f"Event added: {name_msg.content} on {date_msg.content}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

# Run the bot
bot.run(TOKEN)