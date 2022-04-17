import discord, requests, aiofiles, random, urllib, json
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from math import factorial
from mojang import MojangAPI

try:
    from sympy.mpmath import mp
except ImportError:
    from mpmath import mp

client = commands.Bot(command_prefix="g/")
key = ""
client.warnings = {}

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page, colour=0xb27b56)
            await destination.send(embed=embed)
client.help_command = MyNewHelp()

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game("Luz's Pet, My prefix is !g"))
    for guild in client.guilds:
        async with aiofiles.open(f"{guild.id}.txt", mode="a"):
            pass
        client.warnings[guild.id] = {}
    for guild in client.guilds:
        async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
            lines = await file.readlines()
            for line in lines:
                data = line.split(" ")
                member_id = int(data[0])
                admin_id = int(data[1])
                reason = " ".join(data[2:]).strip("\n")
                try:
                    client.warnings[guild.id][member_id][0] += 1
                    client.warnings[guild.id][member_id][1].append((admin_id, reason))
                except KeyError:
                    client.warnings[guild.id][member_id] = [1, [(admin_id, reason)]]
    print("Bot ready!")

@client.event
async def on_guild_join(guild):
    client.warnings[guild.id] = {}

# Auto respond, thanks for Shaqalito#0001 for optimising the code!
auto_responses = {
    "hello": 'Hello there {username}!',
    "gm": 'Good Morning {username}!',
    "gn": 'Good Night {username}!',
    "no u": 'No u',
    "amogus": 'https://tenor.com/view/among-us-twerk-vrchat-among-us-sus-sushi-gif-23196207',
    "rickroll": 'https://tenor.com/view/rick-roll-rick-ashley-never-gonna-give-you-up-gif-22113173',
    "superidol": 'https://tenor.com/view/super-idol-gif-23526928',
    "japanesegoblin": 'https://tenor.com/view/suika-touhou-japanese-goblin-ibuki-gif-23549706',
    "paketphoenix": 'https://tenor.com/view/indi-home-phoenix-indi-home-paket-phoenix-gif-17421920',
    "valveguy": 'https://tenor.com/view/valve-valve-guy-half-life-half-life2-portal-gif-24740578',
    "haram": "https://tenor.com/view/haram-heisenberg-gif-20680378"
}

@client.listen('on_message')
async def autorespond(message):
    user_message = str(message.content)
    if message.author == client.user:
        return
    try:
        await message.channel.send(auto_responses[user_message].replace('{username}', message.author.display_name))
    except KeyError:
        pass

@client.command(help="List of Auto responds")
async def arhelp(ctx):
    mbed = discord.Embed(title="Auto responses", description="hello\ngm\ngn\nno u\namogus\nrickroll\nsuperidol"
                                                             "\njapanesegoblin\npaketphoenix\nvalveguy",
                         colour=0xb27b56)
    await ctx.send(embed=mbed)

@client.command(help="About the bot")
async def aboutme(ctx):
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

# Moderation Commands, thanks for andreawthaderp#5923 and schlöpp#6969 for help!
class Mod(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Delete more than 1 messages")
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=2):
        await ctx.channel.purge(limit=amount+1)

    @clear.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to clear messages.")

    @commands.command(help="Channel nuking") # This is not perfect keep that in mind
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx):
        embed = discord.Embed(
            title=f"Boom! Channel {ctx.channel.name} has been nuked",
            description=f"Nuked by {ctx.author.mention}",
            colour=0xb27b56
        )
        await ctx.channel.delete(reason="Nuke")
        cleanchannel = await ctx.channel.clone(reason="Nuke")
        await cleanchannel.send(embed=embed)

    @nuke.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to drop nukes.")

    @commands.command(help="Warn members")
    @commands.has_permissions(kick_members=True, ban_members=True)
    async def warn(self, ctx, member: discord.Member=None, *, reason="No reason"):
        if member == None:
            await ctx.send("The provided member couldn't be found or you forget to provide one")
        try:
            first_warning = False
            client.warnings[ctx.guild.id][member.id][0] += 1
            client.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))
        except KeyError:
            first_warning = True
            client.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]
        count = client.warnings[ctx.guild.id][member.id][0]
        async with aiofiles.open(f"{ctx.guild.id}.txt", mode="a") as file:
            await file.write(f"{member.id} {ctx.author.id} {reason}\n")
        await ctx.send(f"{member.mention} has been warned for {reason}.\n "
                       f"Now they have {count} {'warn' if first_warning else 'warns'}")

    @warn.error
    async def clear_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to warn.")

    @commands.command(help="Kick members")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason="No reason"):
        await ctx.send(
            member.name + "#" + member.discriminator + " has been kicked from The Grog's Lounge\nReason: " + reason)
        await member.kick(reason=reason)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to kick members.")

    @commands.command(help="Ban members")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await ctx.send(
            member.name + "#" + member.discriminator + " has been banned from The Grog's Lounge\nReason: " + reason)
        await member.ban(reason=reason)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to ban members.")

    @commands.command(help="Unban members")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')
        for ban_entry in banned_users:
            user = ban_entry.user
            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(f'Unbanned {user.mention}')
                return
            await ctx.send(member + " was not found")

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to unban members.")

client.add_cog(Mod(client))

# Meth commands, will be improved along with this project
class Math(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(help="Factorial of...")
    async def factorial(self, ctx, number=1):
        if number<=807:
            result = factorial(number)
            await ctx.send(result)
        else:
            embed = discord.Embed(title="Error",
                                  description="Must be 2000 or fewer in length",
                                  colour=0xe74c3c)
            await ctx.send(embed=embed)

    @commands.command(help="... to the power of 2")
    async def square(self, ctx, number=1):
        square_result = (number * number)
        await ctx.send(square_result)

    @commands.command(help="... to the power of 3")
    async def cube(self, ctx, number=1):
        square_result = (number * number * number)
        await ctx.send(square_result)

    @commands.command(help="Counting Pi")
    async def pi(self, ctx, number=3):
        if number<=1999:
            mp.dps = number
            await ctx.send(mp.pi)
        else:
            embed = discord.Embed(title="Error",
                                  description="Must be 2000 or fewer in length",
                                  colour=0xe74c3c)
            await ctx.send(embed=embed)

client.add_cog(Math(client))

# Fun Commands
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
    async def howcool(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(title=f'How cool is {member.name}#{member.discriminator}?',
                              description=f"{member.mention} is {random.randrange(101)}% cool :sunglasses:",
                              colour=0xb27b56)
        await ctx.send(embed=embed)

    @commands.command(help="The bot will rate how gay you are")
    async def howgay(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(title=f'How gay is {member.name}#{member.discriminator}?',
                              description=f"{member.mention} is {random.randrange(101)}% gay :rainbow_flag:",
                              colour=0xb27b56)
        await ctx.send(embed=embed)

    @commands.command(help="The bot knows your pp size :flushed:")
    async def pp(self, ctx, member: discord.Member = None):
        if member == None:
            member = ctx.author
        embed = discord.Embed(title=f"How long is {member.name}#{member.discriminator}'s pp?",
                              description=f"{member.mention}'s pp is {random.randrange(20)}cm :flushed:",
                              colour=0xb27b56)
        await ctx.send(embed=embed)

    @commands.command(help="Kill someone")
    async def kill(self, ctx, member:discord.Member = None):
        author = ctx.author
        if member == None:
            await ctx.send(f'{author.name} killed themselves')
        embed = discord.Embed(title='', description=f"{author.mention} kills {member.mention}",
                              colour=0xb27b56)
        await ctx.send(embed=embed)

    @commands.command(help="Kiss someone")
    async def kiss(self, ctx, member:discord.Member = None):
        author = ctx.author
        if member == None:
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


client.add_cog(Fun(client))

# Image commands
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
    async def avatar(self, ctx, member: discord.Member = None):
        if member == None:
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

client.add_cog(Image(client))

# Misc commands
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
        await ctx.send("Pong! {0}".format(round(client.latency, 1)))

    @commands.command()
    async def whois(self, ctx, member: discord.Member=None):
        if member == None:
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

client.add_cog(Misc(client))


# Run the bot
client.run(key)
