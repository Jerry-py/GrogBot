import discord
import json, urllib
from io import BytesIO
from discord.ext import commands
from typing import Optional
from PIL import Image

class Pictures(commands.Cog):
    def __init__(self, client):
        self.client = client

    @property
    def _session(self):
        return self.client.http._HTTPClient__session

    async def get_data(self, data_type: str = "json", url: str = None):
        response = await self._session.get(url)
        datatype = data_type.lower()
        if datatype == "json":
            return await response.json()
        elif 'text' in data_type:
            return await response.text()
        elif 'image' in data_type:
            return response
        else:
            return 400

    @commands.command(help="Generate memes from random meme subreddits", aliases=['memes'])
    async def meme(self, ctx):
        memeapi = urllib.request.urlopen('https://meme-api.herokuapp.com/gimme')
        memedata = json.load(memeapi)

        memeurl = memedata['url']
        memename = memedata['title']
        memeposter = memedata['author']
        memesubreddit = memedata['subreddit']

        embed = discord.Embed(title=memename,
                              description=f"Meme by {memeposter} from Subreddit {memesubreddit}",
                              colour=0xb27b56)
        embed.set_image(url=memeurl)
        await ctx.send(embed=embed)

    @commands.command(help="Random cat image")
    async def cat(self, ctx):
        catapi = urllib.request.urlopen('https://some-random-api.ml/animal/cat')
        catdata = json.load(catapi)

        image = catdata['image']
        fact = catdata['fact']

        embed = discord.Embed(title="Meow! Here's a cat",
                              description=f'Did you know? {fact}',
                              colour=0xb27b56)
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command(help="Random dog image")
    async def dog(self, ctx):
        dogapi = urllib.request.urlopen('https://some-random-api.ml/animal/dog')
        dogdata = json.load(dogapi)

        image = dogdata['image']
        fact = dogdata['fact']

        embed = discord.Embed(title="Woof! Here's a dog",
                              description=f'Did you know? {fact}',
                              colour=0xb27b56)
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command(help="Random cat image")
    async def fox(self, ctx):
        foxapi = urllib.request.urlopen('https://some-random-api.ml/animal/fox')
        foxdata = json.load(foxapi)

        image = foxdata['image']
        fact = foxdata['fact']

        embed = discord.Embed(title="(idk what the fox says)! Here's a fox",
                              description=f'Did you know? {fact}',
                              colour=0xb27b56)
        embed.set_image(url=image)
        await ctx.send(embed=embed)

    @commands.command(help="Get user's avatars")
    async def avatar(self, ctx, member: Optional[discord.Member]):
        if member is None:
            member = ctx.author
        member_avatar = member.avatar.url
        embed = discord.Embed(title=f"{member.name}#{member.discriminator}'s avatar", colour=0xb27b56)
        embed.set_image(url=member_avatar)
        await ctx.send(embed=embed)

    @commands.command(description="This command makes anyone *inverted*.")
    async def invert(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        invertImage = await self.get_data('image', f'https://some-random-api.ml/canvas/invert?avatar='
                                                   f'{member.avatar.replace(size=1024, format="png")}')
        imageData = BytesIO(await invertImage.read())

        await ctx.send(file=discord.File(imageData, 'invert.png'))

    @commands.command(description="This command makes anyone *greyscale*.")
    async def greyscale(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        invertImage = await self.get_data('image', f'https://some-random-api.ml/canvas/greyscale?avatar='
                                                   f'{member.avatar.replace(size=1024, format="png")}')
        imageData = BytesIO(await invertImage.read())

        await ctx.send(file=discord.File(imageData, 'invert.png'))

    @commands.command(description="Marry someone")
    async def marry(self, ctx, member:discord.Member = None):
        if member == None:
            await ctx.send("You have to marry someone")
        marriage = Image.open(r"C:\Users\tirfa\Documents\GrogBot-main\core\cogs\pics\thing.jpg")
        asset1 = ctx.author.display_avatar.with_size(128)
        data1 = BytesIO(await asset1.read())
        pfp1 = Image.open(data1)
        pfp1 = pfp1.resize((54,54))

        asset2 = member.display_avatar.with_size(128)
        data2 = BytesIO(await asset2.read())
        pfp2 = Image.open(data2)
        pfp2 = pfp2.resize((54, 54))

        marriage.paste(pfp1, (140, 21))
        marriage.paste(pfp2, (262, 20))

        marriage.save("Married.jpg")
        await ctx.send(file=discord.File("Married.jpg"))

async def setup(client):
    await client.add_cog(Pictures(client))