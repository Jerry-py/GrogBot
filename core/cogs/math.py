import discord
import math
from discord.ext import commands
from typing import Union
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
            result = math.factorial(number)
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

    @commands.group(help="Trigonometry\nFunctions : sin, sinh, asin, asinh, cos, cosh, acos, acosh, tan, tanh, atan, atanh\nNumbers in radians",
                      aliases=["trig", "trigon", "trigonom"])
    async def trigonometry(self, ctx, method=None, number=0):
        mbed = discord.Embed(title="Trigonometry Commands",
                            description="""
                            Trigonometry\nFunctions : `sin`, `sinh`, `asin`, `asinh`, `cos`, `cosh`, `acos`, `acosh`, `tan`, `tanh`, `atan`, `atanh`\nNumbers in radians
                            """
                        )

        await ctx.send(embed=mbed)
    
    @trigonometry.command()
    async def sin(self, ctx, num : Union[int, float]):
        return await ctx.send(math.sin(num))

    @trigonometry.command()
    async def sinh(self, ctx, num : Union[int, float]):
        return await ctx.send(math.sinh(num))

    @trigonometry.command()
    async def asin(self, ctx, num : Union[int, float]):
        return await ctx.send(math.asin(num))
    
    @trigonometry.command()
    async def asinh(self, ctx, num : Union[int, float]):
        return await ctx.send(math.asinh(num))
    
    @trigonometry.command()
    async def cos(self, ctx, num : Union[int, float]):
        return await ctx.send(math.cos(num))

    @trigonometry.command()
    async def cosh(self, ctx, num : Union[int, float]):
        return await ctx.send(math.cosh(num))
    
    @trigonometry.command()
    async def acos(self, ctx, num : Union[int, float]):
        return await ctx.send(math.acos(num))

    @trigonometry.command()
    async def acosh(self, ctx, num : Union[int, float]):
        return await ctx.send(math.acosh(num))
    
    @trigonometry.command()
    async def tan(self, ctx, num : Union[int, float]):
        return await ctx.send(math.tan(num))

    @trigonometry.command()
    async def tanh(self, ctx, num : Union[int, float]):
        return await ctx.send(math.tanh(num))

    @trigonometry.command()
    async def atan(self, ctx, num : Union[int, float]):
        return await ctx.send(math.atan(num))
    
    @trigonometry.command()
    async def atanh(self, ctx, num : Union[int, float]):
        return await ctx.send(math.atanh(num))

def setup(client):
    client.add_cog(Math(client))