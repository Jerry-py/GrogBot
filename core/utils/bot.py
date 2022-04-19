import asyncio
import aiofiles
import discord
from .helpcommand import MyNewHelp
from discord.ext import commands

initial_extension = [
    'core.cogs.chatbot',
    'core.cogs.fun',
    'core.cogs.images',
    'core.cogs.math',
    'core.cogs.misc',
    'core.cogs.moderation',
]

class Grogbotdotpy(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=commands.when_mentioned_or('g/'),
            intents=discord.Intents.all()
        )
        self.help_command = MyNewHelp()
        self.warnings = {}
        self.key = "token"

    async def on_ready(self):
        await self.change_presence(status=discord.Status.online, activity=discord.Game("Luz's Pet, My prefix is !g"))
        for guild in self.guilds:
            async with aiofiles.open(f"{guild.id}.txt", mode="a"):
                pass
            self.warnings[guild.id] = {}
        for guild in self.guilds:
            async with aiofiles.open(f"{guild.id}.txt", mode="r") as file:
                lines = await file.readlines()
                for line in lines:
                    data = line.split(" ")
                    member_id = int(data[0])
                    admin_id = int(data[1])
                    reason = " ".join(data[2:]).strip("\n")
                    try:
                        self.warnings[guild.id][member_id][0] += 1
                        self.warnings[guild.id][member_id][1].append((admin_id, reason))
                    except KeyError:
                        self.warnings[guild.id][member_id] = [1, [(admin_id, reason)]]
        print("Bot ready!")
    
    async def on_guild_join(self, guild):
        self.warnings[guild.id] = {}

    async def load_cogs(self):
        for extension in initial_extension:
            try:
                await self.load_extension(extension)
            except Exception as e:
                print(f"Could not load extension: {extension}.\n\nError: {e}")

    def run(self):
        asyncio.run(self.load_cogs())

        super().run(self.key, reconnect=True)
