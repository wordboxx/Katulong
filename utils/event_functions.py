import json
from datetime import datetime
from pathlib import Path
import discord
from discord import ui

# Constants
EVENTS_FILE = Path("data/events.json")

def date_checker(date):
    """Check if the date is valid."""
    try:
        input_date = datetime.strptime(date, "%m/%d/%Y")
        current_date = datetime.now()
        if input_date.date() < current_date.date():
            return False
        return True
    except ValueError:
        return False

def ensure_events_file():
    """Ensure the events file exists and is properly initialized."""
    EVENTS_FILE.parent.mkdir(exist_ok=True)
    if not EVENTS_FILE.exists():
        EVENTS_FILE.write_text('[]')

def get_events():
    """Get all events from the JSON file."""
    ensure_events_file()
    return json.loads(EVENTS_FILE.read_text())

def save_events(events):
    """Save events to the JSON file."""
    EVENTS_FILE.write_text(json.dumps(events, indent=4))

class EventModal(ui.Modal, title="Add New Event"):
    name = ui.TextInput(label="Event Name", placeholder="Enter the event name...", required=True)
    date = ui.TextInput(label="Event Date", placeholder="MM/DD/YYYY", required=True)

    async def on_submit(self, interaction: discord.Interaction):
        if not date_checker(self.date.value):
            await interaction.response.send_message("Invalid date format or date is in the past. Please use MM/DD/YYYY.", ephemeral=True)
            return
            
        events = get_events()
        events.append({"name": self.name.value, "date": self.date.value})
        save_events(events)
        await interaction.response.send_message(f"Event added: {self.name.value} on {self.date.value}")

class EventSelectView(ui.View):
    def __init__(self, events):
        super().__init__()
        self.events = events
        
        self.select = ui.Select(placeholder="Choose an event to delete")
        for i, event in enumerate(events):
            self.select.add_option(label=event['name'], value=str(i), description=f"Date: {event['date']}")
        self.select.callback = self.select_callback
        self.add_item(self.select)
        
    async def select_callback(self, interaction: discord.Interaction):
        index = int(self.select.values[0])
        event_name = self.events[index]['name']
        self.events.pop(index)
        save_events(self.events)
        await interaction.response.send_message(f'Event "{event_name}" deleted.', ephemeral=True)
        self.stop()

async def add_new_event(interaction: discord.Interaction, bot):
    """Add a new event using a modal."""
    modal = EventModal()
    await interaction.response.send_modal(modal)

async def remove_event(interaction: discord.Interaction, bot):
    """Delete an event using a select menu."""
    events = get_events()
    if not events:
        await interaction.response.send_message("No events to delete.", ephemeral=True)
        return

    view = EventSelectView(events)
    await interaction.response.send_message("Select an event to delete:", view=view, ephemeral=True)

def format_events(events):
    """Format events for display."""
    if not events:
        return "No events scheduled."
    return "**Upcoming Events:**\n" + "\n".join(f"{i+1}. {e['name']} - {e['date']}" for i, e in enumerate(events))

def events_countdown(events):
    """Calculate the time until events.
    
    Args:
        events: List of events or a single event dictionary
        
    Returns:
        str: A formatted string describing the time until each event in years, months, and/or days."""
    if not events:
        return "No events scheduled."
        
    if isinstance(events, dict):
        events = [events]
        
    countdowns = []
    for event in events:
        event_date = datetime.strptime(event['date'], "%m/%d/%Y")
        current_date = datetime.now()
        time_until = event_date - current_date
        
        days = time_until.days
        
        if days < 30:  # Less than a month
            time_str = f"{days} day{'s' if days != 1 else ''}"
        elif days < 365:  # Less than a year
            months = days // 30
            remaining_days = days % 30
            if remaining_days == 0:
                time_str = f"{months} month{'s' if months != 1 else ''}"
            else:
                time_str = f"{months} month{'s' if months != 1 else ''} and {remaining_days} day{'s' if remaining_days != 1 else ''}"
        else:  # More than a year
            years = days // 365
            remaining_days = days % 365
            months = remaining_days // 30
            remaining_days = remaining_days % 30
            
            time_str = f"{years} year{'s' if years != 1 else ''}"
            if months > 0:
                time_str += f", {months} month{'s' if months != 1 else ''}"
            if remaining_days > 0:
                time_str += f" and {remaining_days} day{'s' if remaining_days != 1 else ''}"
                
        countdowns.append(f"• **{event['name']}** ({event['date']}): {time_str}")
    
    return "\n".join(countdowns)