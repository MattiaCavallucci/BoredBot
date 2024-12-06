import discord
import datetime
import os
import random
import asyncio

class Client(discord.Client):
    async def on_ready(self):
        print(f"logged in as {self.user}")

intents = discord.Intents.default()
intents.message_content = True

client = Client(intents=intents)
client.run("MTMxNDM3MTAzOTQyMTEzNjkyNg.G2RvBx.CPH0Q_q4BNgXuJcDamAyTpk-YUgw0FeKtp64tU")