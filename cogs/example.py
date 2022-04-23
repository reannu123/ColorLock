import discord
from discord.ext import commands

class Example(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Events
    @commands.Cog.listener()
    async def on_ready(self):
        print('BotTest online')

    @commands.Cog.listener()
    async def on_member_join(self,member):
        print(f'{member} has joined a server.')

    @commands.Cog.listener() 
    async def on_member_remove(self,member):
        print(f'{member} has left the server.')

    @commands.Cog.listener()
    async def on_command_error(self,ctx, error):
        if isinstance(error, commands.CommandNotFound):
            await ctx.send('{}, command does not exist.'.format(ctx.author.mention))


    #Commands
    # @commands.command()
    # async def ping(self,ctx):
    #     await ctx.send(f'Pong!')

    @commands.command(aliases = ['kimsses','muak'])
    async def kiss(self,ctx, member : discord.Member, area=''):
        if (area != ''):
          await ctx.send('{} has kissed {} on the {}'.format(ctx.author.mention, member.mention, area))
        else:
          await ctx.send('{} has kissed {}'.format(ctx.author.mention, member.mention))

    @commands.command(aliases = ['hugs','huggies'])
    async def hug(self,ctx, member : discord.Member):
        await ctx.send('{} has hugged {}'.format(ctx.author.mention, member.mention))

    @commands.command(aliases = ['loves','lovings'])
    async def love(self,ctx, member : discord.Member):
        if(str(ctx.author)== "Xpu#0356"):
          await ctx.send('{} loves {} as deep as the universe'.format(ctx.author.mention, member.mention))
        else:
          await ctx.send('{} loves {}'.format(ctx.author.mention, member.mention))

    @commands.command()
    async def miss(self,ctx, member : discord.Member):
        await ctx.send('{} misses you, {}'.format(ctx.author.mention, member.mention))



def setup(client):
    client.add_cog(Example(client))

