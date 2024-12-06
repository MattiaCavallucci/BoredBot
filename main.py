import discord
from database import Database
from datetime import datetime
from dotenv import load_dotenv
import os
import random
import asyncio

load_dotenv()
database = Database()

token = os.getenv("TOKEN")

class Client(discord.Client):
    async def on_ready(self):
        print(f"logged in as {self.user}")

    async def on_message(self, message):
        if message.author == self.user:
            return
        if message.content == "!read":
            messages = database.get_messages_by_author(message.author.name)
            messages_parsed = "\n".join([f"{message[2]} - **su {message[3]}** - **il {message[4]}**" for message in messages])
            await message.channel.send(f"**Da {message.author.name}** \n{messages_parsed}")
            return
        database.insert_message(message.author.name, message.content, message.channel.name)

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run(token)