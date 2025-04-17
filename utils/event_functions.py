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

def format_events(events):
    """Format events for display."""
    if not events:
        return "No events scheduled."
    return "**Upcoming Events:**\n" + "\n".join(f"• {e['name']} - {e['date']}" for e in events)