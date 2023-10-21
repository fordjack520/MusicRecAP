import discord
import responses
import creds

async def send_message(message, user_message):
    try:
        response = responses.handle_response(user_message)
        await message.channel.send(response)
    except Exception as exc:
        print(exc)

def run_bot():
    TOKEN = creds.discord_bot_token
    client = discord.Client()

    @client.event
    async def on_ready():
        print(f"{client.user} is running.")
    
    @client.event
    async def on_message(message):
        if message.author == client.user:
            return
        
        username = str(message.author)[:-2]
        user_message= str(message.content)
        channel = str(message.channel)

        if channel != "bot-allow":
            return

        if "spotify" and "https:" not in user_message:
            return

        print(f'{username} said: {user_message}')

        await send_message(message, user_message)
    
    client.run(TOKEN)