import json
from datetime import datetime
from pathlib import Path

# Constants
EVENTS_FILE = Path("data/events.json")

def date_checker(date):
    """Check if the date is valid."""
    current_date = datetime.now().strftime("%m/%d/%Y")
    try:
        datetime.strptime(date, "%m/%d/%Y")
        if date < current_date:
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

async def add_new_event(ctx, name, date):
    """Add a new event to the events list."""
    events = get_events()
    events.append({"name": name, "date": date})
    save_events(events)

# TODO: See if this works later
async def remove_event(ctx, number):
    """Delete an event from the events list."""
    events = get_events()
    events.pop(int(number) - 1)
    save_events(events)

def format_events(events):
    """Format events for display."""
    if not events:
        return "No events scheduled."
    return "**Upcoming Events:**\n" + "\n".join(f"• {e['name']} - {e['date']}" for e in events)

# TODO: See if this works later
def time_until_event(event):
    """Calculate the time until an event.
    
    Returns:
        str: A formatted string describing the time until the event in years, months, and/or days."""
    event_date = datetime.strptime(event['date'], "%m/%d/%Y")
    current_date = datetime.now()
    time_until = event_date - current_date
    
    days = time_until.days
    
    if days < 30:  # Less than a month
        return f"{days} days"
    elif days < 365:  # Less than a year
        months = days // 30
        remaining_days = days % 30
        if remaining_days == 0:
            return f"{months} months"
        return f"{months} months and {remaining_days} days"
    else:  # More than a year
        years = days // 365
        remaining_days = days % 365
        months = remaining_days // 30
        remaining_days = remaining_days % 30
        
        result = f"{years} year{'s' if years > 1 else ''}"
        if months > 0:
            result += f", {months} month{'s' if months > 1 else ''}"
        if remaining_days > 0:
            result += f" and {remaining_days} day{'s' if remaining_days > 1 else ''}"
        return result