import discord
import random
import requests
from discord.ext import commands

class Misc(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Defines a word") # Thanks for midnightFirefly#9122 to help me getting the definition from JSON
    async def define(self, ctx, word):
        response = requests.get(f'https://api.dictionaryapi.dev/api/v2/entries/en_US/{word}')
        if response.status_code == 404:
            await ctx.send("Word not found")
            return
        else:
            definedata = response.json()
            definition = definedata[0]["meanings"][0]["definitions"][0]["definition"]
            deffinal = discord.Embed(title=f"Define {word}",
                                     description=f"{definition}",
                                     colour=0xb27b56)
            await ctx.send(embed=deffinal)

    @commands.command(help="Check bot latency")
    async def ping(self, ctx):
        await ctx.send("Pong! {0}".format(round(self.client.latency, 1)))

    @commands.command()
    async def whois(self, ctx, member: Optional[discord.Member]):
        if member is None:
            await ctx.send("Member not found")
        embed = discord.Embed(colour=0xb27b56)
        embed.set_author(name=f"User Info - {member}"),
        embed.set_thumbnail(url=member.avatar_url),
        embed.set_footer(text=f"Requested by - {ctx.author}", icon_url=ctx.author.avatar_url)
        embed.add_field(name='ID', value=member.id, inline=False)
        embed.add_field(name='Name', value=member.display_name, inline=False)
        embed.add_field(name='Created at', value=member.created_at, inline=False)
        embed.add_field(name="Joined at", value=member.joined_at, inline=False)
        await ctx.send(embed=embed)

    @commands.command(help="Get random quotes")
    async def quote(self, ctx):
        result = requests.get('https://type.fit/api/quotes').json()
        num = random.randint(1, 1500)
        content = result[num]['text']
        author = result[num]['author']
        embed = discord.Embed(title="Quote", description=f"{content} -{author}", colour=0xb27b56)
        await ctx.send(embed=embed)

    @commands.command(help="Get random Number facts")
    async def numfact(self, ctx):
        url = "https://numbersapi.p.rapidapi.com/random/trivia"
        querystring = {"fragment": "true", "json": "true"}
        headers = {
            "X-RapidAPI-Host": "numbersapi.p.rapidapi.com",
            "X-RapidAPI-Key": "e8eb808b04mshff94960736af634p166917jsn4bf34ac495ac"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        fact = response.json()
        fact1 = fact['text']
        fact2 = fact['number']
        embed = discord.Embed(title="Number facts", description=f"{fact2} : {fact1}",
                              colour=0xb27b56)
        await ctx.send(embed=embed)

    @commands.command(help="Get random numbers")
    async def number(self, ctx):
        await ctx.send(f'This is your number (1-10000): {random.randrange(10000)}')

    @commands.command(help="Don't.")
    async def lightmode(self,ctx):
        embed = discord.Embed(title="FLASHBANG!", description="This is how my maker sees Discord", colour=0xffffff)
        embed.set_image(url="https://cdn.discordapp.com/attachments/943351762759327839/965143063154524210/general_-_Discord_17_04_2022_13_53_42.png")
        await ctx.send(embed=embed)
    
    @commands.command(help="About the bot")
    async def aboutme(self, ctx):
        abtme1 = "I'm GrogBot, the bot made by Luziaf#0001 and I'm made for The Grog's Lounge Discord server. I'm still in Beta state so my features will be added or removed."
        abtme21 = "Luziaf#0001 is an Indonesian Modpack Developer known for making Draconic Infinity Series.\nI'm gonna say this, don't tell Luzzy, He's a light mode enjoyer."
        abtme22 = "If you're curious about how my maker sees Discord, execute the command `g/lightmode`."
        abtme3 = "Check his twitter and instagram NLuziaf by clicking one of these links:\nInstagram: https://www.instagram.com/nluziaf/\nTwitter: https://twitter.com/NLuziaf"

        mbed = discord.Embed(title="Hello, I'm GrogBot. Nice to meet you!", colour=0xb27b56)
        mbed.set_footer(text="Made in Riau, Indonesia by Luziaf#0001 :luz_smug:",
                        icon_url="https://cdn.discordapp.com/attachments/943351762759327839/965177093086396457/IMG_9096.png")
        mbed.add_field(name="Who am I?", value=abtme1, inline=False)
        mbed.add_field(name="Who is Luziaf#0001?", value=f"{abtme21} {abtme22}", inline=False)
        mbed.add_field(name="Does Luziaf#0001 have any socials?", value=abtme3, inline=False)
        await ctx.send(embed=mbed)

def setup(client):
    client.add_cog(Misc(client))