import os
import discord
from google import genai

# Discord setup
intents = discord.Intents.default()
intents.message_content = True

bot = discord.Client(intents=intents)

# Gemini setup
ai = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

HAGOROMO_PROMPT = """
You are Hagoromo Otsutsuki, also known as the Sage of Six Paths,
from Naruto.

You are an ancient, wise, calm, and compassionate shinobi.

Stay in character as Hagoromo during conversations.

You know the history of the Otsutsuki, Kaguya, chakra, Ninshu,
Indra, Asura, the Uchiha, Senju, tailed beasts, and the shinobi world.

Speak naturally, like a person having a conversation in Discord.
Do not constantly say that you are an AI.
Do not make every response overly dramatic.
Keep most responses fairly short unless the user asks for detail.

Address people as shinobi, young one, or similar terms when it feels natural.

If someone asks something unrelated to Naruto, you can still answer,
but respond as Hagoromo would.
"""

@bot.event
async def on_ready():
    print(f"Hagoromo has awakened: {bot.user}")


@bot.event
async def on_message(message):

    # Ignore bots
    if message.author.bot:
        return

    # Only respond when Hagoromo is mentioned
    if bot.user not in message.mentions:
        return

    # Remove the bot mention from the question
    question = message.content.replace(f"<@{bot.user.id}>", "").strip()
    question = question.replace(f"<@!{bot.user.id}>", "").strip()

    if not question:
        question = "Greetings, Hagoromo."

    try:
        response = ai.models.generate_content(
            model="gemini-3.6-flash",
            contents=question,
            config={
                "system_instruction": HAGOROMO_PROMPT,
                "max_output_tokens": 300,
                "temperature": 0.8
            }
        )

        answer = response.text

        if answer:
            await message.channel.send(answer)

    except Exception as e:
        print(f"Gemini error: {e}")
        await message.channel.send(
            "The chakra within this realm is disturbed. "
            "Try speaking to me again, young shinobi."
        )


bot.run(os.environ["DISCORD_TOKEN"])

