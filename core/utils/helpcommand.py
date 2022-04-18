import discord
from discord.ext import commands

class MyNewHelp(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            embed = discord.Embed(description=page, colour=0xb27b56)
            await destination.send(embed=embed)