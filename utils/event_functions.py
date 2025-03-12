# Imports
import discord
from discord.ext import commands
import datetime
import json

# Globals
DATA_DIR = 'data/'
EVENTS_FILEPATH = DATA_DIR + 'events.json'

# Functions
def help():
    print(f"Lists all available commands.")
    
    # List of all commands.
    # TODO: Automate this list.
    command_list = [
        "COMMANDS: ",
        "-----",
        "`!events`: lists all event options"
    ]

    return "\n".join(command_list)

async def events(ctx):
    commands_list = [
        "`!list_events`: Lists all events.",
        "`!add_event`: Add event.",
        "`!remove_event`: Remove event."
    ]
    await ctx.send("`\n`".join(commands_list))

#TODO: bot should be prompted to send messages within the functions to get prompts from user
async def list_events(ctx):
    print(f"Listing events from {EVENTS_FILEPATH}")
    
    # Open JSON
    with open(EVENTS_FILEPATH, 'r') as f:
        events = json.load(f)

    # Populates a list with a formatted string for each entry. 
    # Then, returns all entries as one giant string with newline characters.
    event_list = []
    for index, event in enumerate(events):
        event_list.append(f"`{index}`: {event} - {events[event]}")
    
    if len(event_list) == 0:
        await ctx.send(f"`No events found.`")
    else:
        await ctx.send("\n".join(event_list))

async def add_event(ctx):
    # If the event was not specified in the command, prompt user for event name.
    await ctx.send("Name this event?:")
    event_name = await ctx.bot.wait_for('message', check=lambda message: message.author == ctx.author)
    event_name = event_name.content

    # Enter the date of the event.
    while True:
        await ctx.send("When is the event? `MM-DD-YYYY` or `q` to quit:")
        event_date_input = await ctx.bot.wait_for('message', check=lambda message: message.author == ctx.author)
        event_date_input = event_date_input.content
        if event_date_input == "q":
            print(f"User aborted.")
            return None
        try:
            event_date = datetime.datetime.strptime(event_date_input, "%m-%d-%Y").strftime("%B %d, %Y")
            break
        except ValueError:
            await ctx.send("Invalid input; Please enter is `MM-DD-YYYY`.")

    # Add the event and date to JSON.
    print(f"Adding event: {event_name} on {event_date}")
    with open(EVENTS_FILEPATH, 'r') as f:
        events = json.load(f)

    events[event_name] = event_date

    with open(EVENTS_FILEPATH, 'w') as f:
        json.dump(events, f)

async def remove_event(ctx):
    list_events()

    # Open JSON.
    with open(EVENTS_FILEPATH, 'r') as f:
        events = json.load(f)

    # Check if there are any events to begin with.
    if len(events) == 0:
        print("No events found.")
        return None

    while True:
        try:
            await ctx.send("Which event to delete? Enter the Leftmost number:")
            event_to_delete = await ctx.bot.wait_for('message', check=lambda message: message.author == ctx.author)
            event_to_delete = int(event_to_delete.content)
            break
        except ValueError:
            await ctx.send("Invalid input; please input an integer.")

    # Make sure that selected event is in appropriate range.
    if 0 <= event_to_delete < len(events):
        # Gets event name from index choice to use to delete.
        event_name = list(events.keys())[event_to_delete]
    
        # Delete the event.
        del events[event_name]

        # Write to JSON.
        with open(EVENTS_FILEPATH, 'w') as f:
            json.dump(events, f, indent=4)

    # If range is invalid.
    else:
        await ctx.send("Invalid number; operation aborted.")


# This module provides date-related functions and constants.
if __name__ == "__main__":
    print("This module is not meant to be run directly.")