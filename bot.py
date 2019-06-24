import discord
import json
import aiohttp
import banhammer

generator = banhammer.Generator()

with open('config.json') as j:
    config = json.load(j)

class BotClient(discord.Client):
    async def on_ready(self):
        print('Ready to swing the hammer as', self.user)

client = BotClient()
client.run(config['token'])
