// Imports
const { Client, GatewayIntentBits, Partials, Collection } = require('discord.js');
const { config } = require('dotenv');
const eventFunctions = require('./utils/event_functions');

// Load environment variables.
config({ path: 'data/.env' });

// Setup intents.
const client = new Client({
    intents: [
        GatewayIntentBits.Guilds,
        GatewayIntentBits.GuildMessages,
        GatewayIntentBits.MessageContent,
        GatewayIntentBits.GuildMembers,
        GatewayIntentBits.GuildPresences
    ],
    partials: [Partials.Message, Partials.Channel, Partials.Reaction]
});

// Bot Functions
// --- Logged in.
client.once('ready', () => {
    console.log(`Logged in as ${client.user.tag}!`);
});

// --- If the bot is mentioned in message.
client.on('messageCreate', async (message) => {
    // Don't respond to our own messages.
    if (message.author.bot) return;

    // Check if the bot was mentioned in the message.
    if (message.mentions.has(client.user)) {
        // TODO: Fill out command list when pinged.
        await message.channel.send(eventFunctions.help());
    }

    // This line is important! It processes commands.
    client.commands.get(message.content.split(' ')[0].substring(1))?.execute(message);
});

// Commands (like !ping)
client.commands = new Collection();
client.commands.set('ping', {
    name: 'ping',
    description: 'Test to see if bot is working.',
    async execute(message) {
        await message.channel.send('Pong!');
    }
});
client.commands.set('events', {
    name: 'events',
    description: 'Lists help menu for all events functions.',
    async execute(message) {
        await eventFunctions.events(message);
    }
});
client.commands.set('list_events', {
    name: 'list_events',
    description: 'Lists all events in events.json.',
    async execute(message) {
        await eventFunctions.list_events(message);
    }
});
client.commands.set('add_event', {
    name: 'add_event',
    description: 'Add an event to events.json.',
    async execute(message) {
        await eventFunctions.add_event(message);
    }
});
client.commands.set('remove_event', {
    name: 'remove_event',
    description: 'Removes an event from events.json.',
    async execute(message) {
        await eventFunctions.remove_event(message);
    }
});

// Get token from environment variable.
const TOKEN = process.env.DISCORD_TOKEN;
if (!TOKEN) {
    throw new Error("No token found. Make sure DISCORD_TOKEN is set in .env file");
}

client.login(TOKEN);