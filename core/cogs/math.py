import discord, math
from discord.ext import commands
from typing import Union
try:
    from sympy.mpmath import mp
except ImportError:
    from mpmath import mp

class CalcView(discord.ui.View):
    def __init__(self, ctx : commands.Context, embed : discord.Embed):
        self.ctx = ctx
        self.embed = embed
        self._all_ans = [0]
        self.equation = ""
        super().__init__(timeout=120)
        
    def parse_equation(self):
        new_equation = self.equation.replace("%", " / 100")
        new_equation = new_equation.replace("x", "*")
        new_equation = new_equation.replace("÷", "/")
        new_equation = new_equation.replace("^", "**")
        new_equation = new_equation.replace("Ans", f"{self._all_ans[0]}")
        new_equation = new_equation.replace("π", "3.141592653589793")
        return new_equation    
    
    async def calculate(self):
        """Calculate the equation"""
        log = math.log
        try:
            ans = eval(self.parse_equation())
            self._all_ans[0] = ans
        except Exception as e:
            self._all_ans[0] = 0
            ans = "Error! Make sure you closed your parenthesis and brackets!\n\n Do not do `number(...)` Instead use `number x (...)`\n Do not combine numbers into each other - Ex: `π6^2` Instead do `π*6^2` \n**They Will Result In Different Answers!**\n\nDon't also do leave operations on its own"
        self.equation = ""
        
        return ans
    
    def _remove_placeholder(self):
        self.embed.description = ""
        
    def _placeholder(self):
        self.embed.description = "`Enter your equation below`"
        
    def new_equation(self, value : str):
        self.equation += value
        
    def new_embed(self, value : str):
        self.new_equation(value)
        self.embed.description = f"```{self.equation}```"
        return self.embed
    
    @discord.ui.button(row=0, label="^", style=discord.ButtonStyle.secondary)
    async def power(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the exponent operation to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=0, label="(", style=discord.ButtonStyle.success)
    async def left_parathesis(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the left parenthesis to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=0, label=")", style=discord.ButtonStyle.success)
    async def right_parenthesis(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the right parenthesis to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=0, label="AC", style=discord.ButtonStyle.danger)
    async def ac(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Delete the last character of the equation"""
        await inter.response.defer()
        if len(self.equation) <= 1:
            self._placeholder()
        else:
            self.equation = self.equation.rstrip(self.equation[-1])
            self.embed.description = self.equation
        await inter.edit_original_message(embed=self.embed)
    
    @discord.ui.button(row=0, label="CE", style=discord.ButtonStyle.danger)
    async def ce(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Clear the equation"""
        await inter.response.defer()
        self._placeholder()
        self.equation = ""
        await inter.edit_original_message(embed=self.embed)
    
    @discord.ui.button(row=1, label="%", style=discord.ButtonStyle.secondary)
    async def percentage(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the percentage operation to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=1, label="7", style=discord.ButtonStyle.success)
    async def seven(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the number 7 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=1, label="8", style=discord.ButtonStyle.success)
    async def eight(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the number 8 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=1, label="9", style=discord.ButtonStyle.success)
    async def nine(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the number 9 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=1, label="÷", style=discord.ButtonStyle.secondary)
    async def divide(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the division operation to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=2, label="Ans", style=discord.ButtonStyle.secondary)
    async def ans(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Get previous answer"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=2, label="6", style=discord.ButtonStyle.success)
    async def six(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the number 6 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=2, label="5", style=discord.ButtonStyle.success)
    async def five(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the number 5 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=2, label="4", style=discord.ButtonStyle.success)
    async def four(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the number 4 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=2, label="x", style=discord.ButtonStyle.secondary)
    async def multiply(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the mutiplication operation to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=3, label="log(", style=discord.ButtonStyle.secondary)
    async def log(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the sin math function to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=3, label="3", style=discord.ButtonStyle.success)
    async def three(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the number 3 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=3, label="2", style=discord.ButtonStyle.success)
    async def two(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the number 2 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=3, label="1", style=discord.ButtonStyle.success)
    async def one(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the number 1 to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=3, label="-", style=discord.ButtonStyle.secondary)
    async def subtract(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add the subtract operation to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=4, label="π", style=discord.ButtonStyle.secondary)
    async def pi(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add Cos math function"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=4, label="0", style=discord.ButtonStyle.success)
    async def zero(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add zero to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    @discord.ui.button(row=4, label="(.)", style=discord.ButtonStyle.secondary)
    async def decimal(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Add a decimal to the equation"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed('.'))
    
    @discord.ui.button(row=4, label="=", style=discord.ButtonStyle.primary)
    async def solve(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Solve the equation"""
        await inter.response.defer()
        ans = await self.calculate()
        self.embed.description = str(ans)
        await inter.edit_original_message(embed=self.embed)
    
    @discord.ui.button(row=4, label="+", style=discord.ButtonStyle.secondary)
    async def add(self, inter : discord.InteractionResponse, button : discord.ui.Button):
        """Math Add operation Button"""
        await inter.response.defer()
        await inter.edit_original_message(embed=self.new_embed(button.label))
    
    async def interaction_check(self, inter : discord.InteractionResponse):
        """Check if the user who used the the interaction is the author of the message"""
        if inter.user == self.ctx.author:
            return True
        await inter.response.send_message("Hey! You can't do that!", ephemeral=True)
        return False


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

    @commands.command()
    async def tau(self, ctx, number=3):
        if number<=1999:
            mp.dps = number
            await ctx.send(mp.pi*2)
        else:
            embed = discord.Embed(title="Error",
                                  description="Must be 2000 or fewer in length",
                                  colour=0xe74c3c)
            await ctx.send(embed=embed)

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

    @commands.command(name='calc', aliases=['calculate', 'calculator'])
    async def calc(self, ctx : commands.Context):
        embed = discord.Embed(title='Calculator', description='`Enter your equation below`',
                              colour=0xb27b56)
        await ctx.send(embed=embed, view=CalcView(ctx, embed))

async def setup(client):
    await client.add_cog(Math(client))