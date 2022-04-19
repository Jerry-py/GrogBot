import aiofiles
import discord
from discord.ext import commands
from discord.ext.commands import MissingPermissions
from typing import Optional, Union


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
    async def warn(self, ctx, member: Optional[discord.Member], *, reason="No reason"):
        if member is None:
            await ctx.send("The provided member couldn't be found or you forget to provide one")
        try:
            first_warning = False
            self.client.warnings[ctx.guild.id][member.id][0] += 1
            self.client.warnings[ctx.guild.id][member.id][1].append((ctx.author.id, reason))
        except KeyError:
            first_warning = True
            self.client.warnings[ctx.guild.id][member.id] = [1, [(ctx.author.id, reason)]]
        count = self.client.warnings[ctx.guild.id][member.id][0]
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
        await ctx.send(f'{member.name}#{member.discriminator}' + " has been kicked from The Grog's Lounge\nReason: " + reason)

        await member.kick(reason=reason)

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to kick members.")

    @commands.command(help="Ban members")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason="No reason"):
        await ctx.send(f'{member.name}#{member.discriminator}' + " has been banned from The Grog's Lounge\nReason: " + reason)

        await member.ban(reason=reason)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to ban members.")

    @commands.command(help="Unban members")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member : Union[int, str]):
        if member is int:
            try:
                await ctx.guild.unban(discord.Object(id=member))
                return await ctx.send(f'Unbanned {user}')
            except Exception:
                await ctx.send(f'{member} was not found in the banned list')

        else:
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split('#')

            for ban_entry in banned_users:
                user = ban_entry.banned_users

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    return await ctx.send(f'Unbanned {user}')

        await ctx.send(f'{member} was not found in the banned list')

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, MissingPermissions):
            await ctx.send("You don't have permission to unban members.")

async def setup(client):
    await client.add_cog(Mod(client))