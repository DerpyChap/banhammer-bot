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
        async with session.post('https://api.imgur.com/3/image', data=data, headers={'Authorization': f'Client-ID {config["client_id"]}'}) as resp:
            if resp.status != 200:
                return
            d = await resp.json()
            if d['success']:
                return d['data']['link']
            return

class BotClient(discord.Client):
    async def on_ready(self):
        print('Ready to swing the hammer as', self.user)
    
    async def on_member_ban(self, guild: discord.Guild, member: discord.Member):
        sys_channel = guild.system_channel
        # No system channel, so don't continue
        if not sys_channel:
            return

        # Check the bot's permissions to make sure it can post images
        permissions = sys_channel.permissions_for(guild.me)
        if not (permissions.read_messages and permissions.send_messages and permissions.embed_links):
            return
        
        # Generate the image in an executor because PIL is blocking
        image = await self.loop.run_in_executor(None, generator.image_gen, member.name)

        # Upload the image to Imgur
        url = await upload(image)

        # Send the message to Discord
        if url:
            embed = discord.Embed()
            embed.set_image(url=url)
            await sys_channel.send(f'**{member.name} has been smitten by Tom Scott\'s Banhammer**', embed=embed)

client = BotClient()
client.run(config['token'])
