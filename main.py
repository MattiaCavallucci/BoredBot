import discord
from discord.ext import commands
from database import Database
from dotenv import load_dotenv
import os

load_dotenv()

def run():

    token = os.getenv("TOKEN")
    database = Database()
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_ready():
        await bot.tree.sync()
        print(f"logged in as {bot.user}")

    @bot.event
    async def on_message(message):
        if message.author == bot.user:
            return
        
        database.insert_message(message.author.name, message.content, message.channel.name)
        await bot.process_commands(message)

    @bot.tree.command(name="read", description="Reads all messages from the user")
    async def read(interaction: discord.Interaction):
        messages = database.get_messages_by_author(interaction.user.name)
        messages_parsed = "\n".join([f"{message[2]} - **Su {message[3]}** - **Il {message[4]}**" for message in messages])
        await interaction.response.send_message("Done!", ephemeral=True)
        await interaction.user.send(f"**Da {interaction.user.name}** \n{messages_parsed}")

    @bot.tree.command(name="echo", description="Echoes a message")
    async def echo(interaction: discord.Interaction, message: str):
        await interaction.response.send_message("Echoing...", ephemeral=True)
        await interaction.channel.send(message)


    bot.run(token)

if __name__ == "__main__":
    run()