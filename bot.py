from datetime import datetime, timedelta
import discord
from discord.ext import commands
import responses
import creds

async def send_message(message, user_message, quiet):
    try:
        timestamp = message.created_at - timedelta(hours=8)
        time = timestamp.strftime("%m/%d/%Y %H:%M:%S")
        response = responses.handle_response(user_message, str(message.author)[:-2], time, quiet)
        if quiet == False:
            await message.channel.send(response)

    except Exception as exc:
        print(exc)

def run_bot():
    TOKEN = creds.discord_bot_token
    client = commands.Bot(command_prefix="~")

    @client.event
    async def on_ready():
        print(f"{client.user} is running.")
    
    @client.event
    async def on_message(message):
        await client.process_commands(message)
        if message.author == client.user:
            return
        
        username = str(message.author)[:-2]
        user_message= str(message.content)
        channel = str(message.channel)

        if channel != "music-recs":
            return

        if "spotify" and "https:" not in user_message:
            return

        print(f'{username} said: {user_message}')

        await send_message(message, user_message, quiet=False)
    
    @client.command()
    async def full_sweep(ctx):
        if str(ctx.channel) != "music-recs":
            print(f'Full sweep attempted in \"{ctx.channel}\"')
            return
        if str(ctx.author)[:-2] != "chubbypapaya":
            print(f'Full sweep attempted by {ctx.author}')
            return
        counter = 0
        async for message in ctx.channel.history(limit=500):
            if "spotify" in str(message.content):
                await send_message(message,str(message.content),quiet=True)
                counter += 1
        await ctx.channel.send(f"{counter} items have been successfully added to the spreadsheet! {ctx.channel}")
        print(f'Full sweep: {counter} items.')
    
    client.run(TOKEN)