import discord
from discord.ext import commands
import discord.ext.commands
from database import Database
from dotenv import load_dotenv
import os

import discord.ext

load_dotenv()

def run():
    token = os.getenv("TOKEN")
    database = Database()
    intents = discord.Intents.all()
    bot = commands.Bot(command_prefix="!", intents=intents)

    @bot.event
    async def on_guild_join(guild: discord.Guild):
        for channel in guild.text_channels:
            if channel.name == "tickets":
                return
            else:
                await guild.create_text_channel(name="tickets", overwrites={guild.default_role: discord.PermissionOverwrite(read_messages=False)}, position=0)

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

    @bot.tree.command(name="read_message_history", description="DMs all messages from a specified user")
    async def read_msgs(interaction: discord.Interaction, user: str):
        messages = database.get_messages_by_author(user)
        messages_parsed = "\n".join([f"{message[2]} - **Su {message[3]}** - **Il {message[4]}**" for message in messages])
        await interaction.response.send_message("Done!", ephemeral=True)
        await interaction.user.send(f"**Da {user}** \n{messages_parsed}")

    @bot.tree.command(name="echo", description="Echoes a message")
    async def echo(interaction: discord.Interaction, message: str):
        await interaction.response.send_message("Echoing...", ephemeral=True)
        await interaction.channel.send(message)

    @bot.tree.command(name="open_ticket", description="Opens a new ticket")
    async def open_ticket(interaction: discord.Interaction):
        channel = discord.utils.get(interaction.guild.text_channels, name="tickets")
        await channel.edit(overwrites={interaction.guild.default_role: discord.PermissionOverwrite(read_messages=False)})

        if discord.utils.get(channel.threads, name=f"ticket-{interaction.user.name}"):
            await interaction.response.send_message("You already have an open ticket!", ephemeral=True)
            return
        
        thread = await channel.create_thread(name=f"ticket-{interaction.user.name}", type=discord.ChannelType.private_thread)
        await thread.send(f"Welcome to your ticket, {interaction.user.mention}!")
        await interaction.response.send_message("Ticket opened!", ephemeral=True)

    # @bot.tree.command(name="close_ticket", description="Closes a ticket")
    # @commands.has_permissions(administrator=True)
    # async def close_ticket(interaction: discord.Interaction):
    #     await interaction.response.send_message("Closing ticket...", ephemeral=True)


    bot.run(token)

if __name__ == "__main__":
    run()

#TODO: Implement guild logic into database and bot