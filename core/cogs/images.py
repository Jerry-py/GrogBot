import discord
import json, urllib
from discord.ext import commands
from mojang import MojangAPI
from typing import Optional

class Image(commands.Cog):
    def __init__(self, client):
        self.client = client

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

    @commands.command(help="Get user's avatars")
    async def avatar(self, ctx, member: Optional[discord.Member]):
        if member is None:
            member = ctx.author
        member_avatar = member.avatar_url
        embed = discord.Embed(title=f"{member.name}#{member.discriminator}'s avatar", colour=0xb27b56)
        embed.set_image(url=member_avatar)
        await ctx.send(embed=embed)

    @commands.command(help="Get Minecraft skin")
    async def mcskin(self, ctx, player: str):
        uuid = MojangAPI.get_uuid(player)

        embed = discord.Embed(colour=0xb27b56)
        embed.set_author(name=f"Player skin - {player}")
        embed.add_field(name="UUID", value=uuid, inline=False)
        embed.add_field(name="Skin", value=f'https://crafatar.com/skins/{uuid}', inline=False)
        await ctx.send(embed=embed)

async def setup(client):
    await client.add_cog(Image(client))