# Imports
import discord
from discord.ext import commands
import datetime
import json

# Globals
DATA_DIR = 'data/'
EVENTS_FILEPATH = DATA_DIR + 'events.json'

# Functions
def events():
    commands_list = [
        "list_events: Lists all events.",
        "add_event: Add event.",
        "remove_event: Remove event."
    ]
    return "\n".join(commands_list)

def list_events():
    print(f"Listing events from {EVENTS_FILEPATH}")
    
    # Open JSON
    with open(EVENTS_FILEPATH, 'r') as f:
        events = json.load(f)

    # Populates a list with a formatted string for each entry. 
    # Then, returns all entries as one giant string with newline characters.
    event_list = []
    for index, event in enumerate(events):
        event_list.append(f"{index}: {event} - {events[event]}")
    
    return "\n".join(event_list)

def add_event(event_name=""):
    # If the event was not specified in the command, prompt user for event name.
    if event_name == "":
        event_name = input("What do you want to call this event?: ")
    
    # Enter the date of the event.
    while True:
        event_date_input = input("When is the event? (MM-DD-YYYY): ")
        try:
            event_date = datetime.datetime.strptime(event_date_input, "%m-%d-%Y").strftime("%B %d, %Y")
            break
        except ValueError:
            print("Invalid date format. Please enter in MM-DD-YYYY format.")

    # Add the event and date to JSON.
    print(f"Adding event: {event_name} on {event_date}")
    with open(EVENTS_FILEPATH, 'r') as f:
        events = json.load(f)

    events[event_name] = event_date

    with open(EVENTS_FILEPATH, 'w') as f:
        json.dump(events, f)

def remove_event():
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
            event_to_delete = int(input("Which event to delete? Select number: "))
            break
        except ValueError:
            print("Invalid input. Please enter a valid number.")


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
        print("Invalid number.")



# This module provides date-related functions and constants.
if __name__ == "__main__":
    print("This module is not meant to be run directly.")