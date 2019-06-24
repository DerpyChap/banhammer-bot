import discord
import json
import aiohttp
import banhammer

generator = banhammer.Generator()

with open('config.json') as j:
    config = json.load(j)

async def upload(b):
    """Upload stuff to Imgur because the GIFs are like 1 MB too large for Discord"""
    data = aiohttp.FormData(quote_fields=False)
    data.add_field('image',
                    b,
                    filename='banned.gif',
                    content_type='image/gif')
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.imgur.com/3/image', data=data, headers={'Authorization': config['client_id']}) as resp:
            if resp.status != 200:
                return
            d = await resp.json()
            if d['success']:
                return d['data']['link']
            return

class BotClient(discord.Client):
    async def on_ready(self):
        print('Ready to swing the hammer as', self.user)

client = BotClient()
client.run(config['token'])
