import os
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"Hagoromo has awakened: {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "hagoromo" in message.content.lower():
        await message.channel.send(
            "I am Hagoromo Ōtsutsuki, the Sage of Six Paths. "
            "What wisdom do you seek, young shinobi?"
        )

client.run(os.environ["DISCORD_TOKEN"])
