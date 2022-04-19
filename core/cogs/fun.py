import asyncio
import discord
import os
import random
import urllib.request
from discord.ext import commands
from typing import Optional

class Fun(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Ask something", aliases=['8ball', '8b'])
    async def eightball(self, ctx, *, question):
        responses = ["As I see it, yes.", "Ask again later.", "Better not tell you now.", "Cannot predict now.",
                     "Concentrate and ask again.",
                     "Don’t count on it.", "It is certain.", "It is decidedly so.", "Most likely.", "My reply is no.",
                     "My sources say no.",
                     "Outlook not so good.", "Outlook good.", "Reply hazy, try again.", "Signs point to yes.",
                     "Very doubtful.", "Without a doubt.",
                     "Yes.", "Yes – definitely.", "You may rely on it."]
        response = random.choice(responses)
        embed = discord.Embed(title='', description=f'Question : {question}\nAnswer : {response}', colour=0xb27b56)
        await ctx.send(embed=embed)

    @commands.command(help="Lowercase the message")
    async def lower(self, ctx, msg):
        transformed = msg.lower()
        await ctx.send(transformed)

    @commands.command(help="Uppercase the message")
    async def upper(self, ctx, msg):
        transformed = msg.upper()
        await ctx.send(transformed)

    @commands.command(help="Spell backwards")
    async def reverse(self, ctx, msg):
        transformed = reversed(msg)
        await ctx.send(''.join(transformed))

    @commands.command(help="The bot will rate how cool you are")
    async def howcool(self, ctx, member: Optional[discord.Member]):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f'How cool is {member.name}#{member.discriminator}?',
                              description=f"{member.mention} is {random.randrange(101)}% cool :sunglasses:",
                              colour=0xb27b56)
        await ctx.send(embed=embed)

    @commands.command(help="The bot will rate how gay you are")
    async def howgay(self, ctx, member: Optional[discord.Member]):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f'How gay is {member.name}#{member.discriminator}?',
                              description=f"{member.mention} is {random.randrange(101)}% gay :rainbow_flag:",
                              colour=0xb27b56)
        await ctx.send(embed=embed)

    @commands.command(help="The bot knows your pp size :flushed:")
    async def pp(self, ctx, member: Optional[discord.Member]):
        if member is None:
            member = ctx.author
        embed = discord.Embed(title=f"How long is {member.name}#{member.discriminator}'s pp?",
                              description=f"{member.mention}'s pp is {random.randrange(20)}cm :flushed:",
                              colour=0xb27b56)
        await ctx.send(embed=embed)

    @commands.command(help="Kill someone")
    async def kill(self, ctx, member: Optional[discord.Member]):
        author = ctx.author
        if member is None:
            await ctx.send(f'{author.name} killed themselves')
        embed = discord.Embed(title='', description=f"{author.mention} kills {member.mention}",
                              colour=0xb27b56)
        await ctx.send(embed=embed)

    @commands.command(help="Kiss someone")
    async def kiss(self, ctx, member: Optional[discord.Member]):
        author = ctx.author
        if member is None:
            await ctx.send(f'{author.name} kissed themselves')
        embed = discord.Embed(title='', description=f"{author.mention} kisses {member.mention}",
                              colour=0xb27b56)
        await ctx.send(embed=embed)

    @commands.command(help="Sending Paradoxes, never think about it")
    async def paradox(self, ctx):
        paradoxes = ["Less is More", "I am nobody", "This sentence is false",
                     "New mission : Refuse the mission", "Does a set of all sets contain itself?",
                     "If you didn't get this message, call me", "I always lie"]
        paradox = random.choice(paradoxes)
        await ctx.send(paradox)
        
    @commands.command(help="Play rock paper scissors")
    async def rps(self, ctx, action):
        possible = ["r", "p", "s"]
        comp = random.choice(possible)

        if action == comp:
            await ctx.send(f"I chose ({comp})")
            await ctx.send("Tie")
        elif action == "r":
            if comp == "s":
                await ctx.send(f"I chose ({comp})")
                await ctx.send("You win")
            if comp == "p":
                await ctx.send(f"I chose ({comp})")
                await ctx.send("You lose")
        elif action == "p":
            if comp == "r":
                await ctx.send(f"I chose ({comp})")
                await ctx.send("You win")
            if comp == "s":
                await ctx.send(f"I chose ({comp})")
                await ctx.send("You lose")
        elif action == "s":
            if comp == "p":
                await ctx.send(f"I chose ({comp})")
                await ctx.send("You win")
            if comp == "r":
                await ctx.send(f"I chose ({comp})")
                await ctx.send("You lose")
        else:
            await ctx.send("Invalid choice")

    @commands.command(name='ttsobama')
    async def _ttsobama(self, ctx, *, text: str = None):
        if text is None:
            return await ctx.send("You need to enter text!")

        if len(text) > 280:
            return await ctx.send("Text is too long!")
        await ctx.send('Your video is loading... Might take up to 5-12 seconds', delete_after=12)

        response = self.session.post(url='http://talkobamato.me/synthesize.py', data={
            "input_text": text
        })
        await asyncio.sleep(12)
        url = response.url.replace('http://talkobamato.me/synthesize.py?speech_key=', '')
        url = f'http://talkobamato.me/synth/output/{url}/obama.mp4'
        await asyncio.sleep(1)
        urllib.request.urlretrieve(url, 'obama.mp4')
        file = discord.File('obama.mp4')
        await ctx.send(file=file)
        os.remove('obama.mp4')

async def setup(client):
    await client.add_cog(Fun(client))