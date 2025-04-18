import json
from datetime import datetime
from pathlib import Path

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

async def add_new_event(ctx, bot):
    """Add a new event with user prompts."""
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
            
        events = get_events()
        events.append({"name": name_msg.content, "date": date_msg.content})
        save_events(events)
        await ctx.send(f"Event added: {name_msg.content} on {date_msg.content}")
    except Exception as e:
        await ctx.send(f"Error: {e}")

async def remove_event(ctx, bot):
    """Delete an event with user prompts."""
    def check(m):
        return m.author == ctx.author and m.channel == ctx.channel

    events = get_events()
    if not events:
        await ctx.send("No events to delete.")
        return

    await ctx.send(f"Enter the event number to delete:\n{format_events(events)}")
    num_msg = await bot.wait_for('message', check=check, timeout=30.0)
    
    if not num_msg.content.isdigit():
        await ctx.send("Invalid input. Please enter a valid number.")
        return
    
    number = int(num_msg.content)
    length = len(events)
    if number > length or number < 1:
        await ctx.send("Invalid event number.")
        return
        
    event_name = events[number - 1]['name']
    events.pop(number - 1)
    save_events(events)
    await ctx.send(f'Event "{event_name}" deleted.')

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