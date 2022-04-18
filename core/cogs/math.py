import discord
from discord.ext import commands
from math import factorial

try:
    from sympy.mpmath import mp
except ImportError:
    from mpmath import mp

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

def setup(client):
    client.add_cog(Math(client))