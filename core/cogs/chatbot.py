import contextlib
import discord
from discord.ext import commands

class Chatbot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.auto_responses = {
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

    @commands.Cog.listener()
    async def on_message(self, message):
        user_message = str(message.content)
        if message.author == self.client.user:
            return
        with contextlib.suppress(KeyError):
            await message.channel.send(self.auto_responses[user_message].replace('{username}', message.author.display_name))

    @commands.command(help="List of Auto responds")
    async def arhelp(self, ctx):
        mbed = discord.Embed(title="Auto responses", 
        description="hello\ngm\ngn\nno u\namogus\nrickroll\nsuperidol"
                                                                "\njapanesegoblin\npaketphoenix\nvalveguy",
                            colour=0xb27b56)
        await ctx.send(embed=mbed)

def setup(client):
    client.add_cog(Chatbot(client))