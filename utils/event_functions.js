// Imports
const { MessageEmbed } = require('discord.js');
const fs = require('fs');
const path = require('path');
const { promisify } = require('util');
const readFile = promisify(fs.readFile);
const writeFile = promisify(fs.writeFile);

// Globals
const DATA_DIR = 'data/';
const EVENTS_FILEPATH = path.join(DATA_DIR, 'events.json');

// Functions
function help() {
    console.log("Lists all available commands.");

    // List of all commands.
    // TODO: Automate this list.
    const commandList = [
        "COMMANDS: ",
        "-----",
        "`!events`: lists all event options"
    ];

    return commandList.join("\n");
}

async function events(message) {
    const commandsList = [
        "`!list_events`: Lists all events.",
        "`!add_event`: Add event.",
        "`!remove_event`: Remove event."
    ];
    await message.channel.send(commandsList.join("\n"));
}

//TODO: bot should be prompted to send messages within the functions to get prompts from user
async function list_events(message) {
    console.log(`Listing events from ${EVENTS_FILEPATH}`);

    // Open JSON
    const events = JSON.parse(await readFile(EVENTS_FILEPATH, 'utf8'));

    // Populates a list with a formatted string for each entry. 
    // Then, returns all entries as one giant string with newline characters.
    const eventList = [];
    for (const [index, event] of Object.entries(events)) {
        eventList.push(`\`${index}\`: ${event} - ${events[event]}`);
    }

    if (eventList.length === 0) {
        await message.channel.send("`No events found.`");
    } else {
        await message.channel.send(eventList.join("\n"));
    }
}

async function add_event(message) {
    // If the event was not specified in the command, prompt user for event name.
    await message.channel.send("Name this event?:");
    const eventName = (await message.channel.awaitMessages({
        filter: m => m.author.id === message.author.id,
        max: 1,
        time: 60000,
        errors: ['time']
    })).first().content;

    // Enter the date of the event.
    let eventDate;
    while (true) {
        await message.channel.send("When is the event? `MM-DD-YYYY` or `q` to quit:");
        const eventDateInput = (await message.channel.awaitMessages({
            filter: m => m.author.id === message.author.id,
            max: 1,
            time: 60000,
            errors: ['time']
        })).first().content;
        if (eventDateInput === "q") {
            console.log("User aborted.");
            return;
        }
        try {
            eventDate = new Date(eventDateInput).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' });
            break;
        } catch (error) {
            await message.channel.send("Invalid input; Please enter is `MM-DD-YYYY`.");
        }
    }

    // Add the event and date to JSON.
    console.log(`Adding event: ${eventName} on ${eventDate}`);
    const events = JSON.parse(await readFile(EVENTS_FILEPATH, 'utf8'));

    events[eventName] = eventDate;

    await writeFile(EVENTS_FILEPATH, JSON.stringify(events, null, 4));
}

async function remove_event(message) {
    await list_events(message);

    // Open JSON.
    const events = JSON.parse(await readFile(EVENTS_FILEPATH, 'utf8'));

    // Check if there are any events to begin with.
    if (Object.keys(events).length === 0) {
        console.log("No events found.");
        return;
    }

    while (true) {
        try {
            await message.channel.send("Which event to delete? Enter the Leftmost number:");
            const eventToDelete = parseInt((await message.channel.awaitMessages({
                filter: m => m.author.id === message.author.id,
                max: 1,
                time: 60000,
                errors: ['time']
            })).first().content, 10);
            if (isNaN(eventToDelete)) throw new Error();
            break;
        } catch (error) {
            await message.channel.send("Invalid input; please input an integer.");
        }
    }

    // Make sure that selected event is in appropriate range.
    const eventNames = Object.keys(events);
    if (eventToDelete >= 0 && eventToDelete < eventNames.length) {
        // Gets event name from index choice to use to delete.
        const eventName = eventNames[eventToDelete];

        // Delete the event.
        delete events[eventName];

        // Write to JSON.
        await writeFile(EVENTS_FILEPATH, JSON.stringify(events, null, 4));
    } else {
        await message.channel.send("Invalid number; operation aborted.");
    }
}

module.exports = {
    help,
    events,
    list_events,
    add_event,
    remove_event
};