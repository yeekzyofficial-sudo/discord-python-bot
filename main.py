import discord
from discord.ext import commands
import os
import asyncio

from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="c.",
    intents=intents,
    help_command=None,
    case_insensitive=True
)

@bot.event
async def on_ready():
    print(f"───────────────────────────────────────────────")
    print(f"Logged in as   : {bot.user}")
    print(f"User ID        : {bot.user.id}")
    print(f"Guilds         : {len(bot.guilds)}")
    print(f"───────────────────────────────────────────────")
    
    await bot.change_presence(
        activity=discord.Game(name="GTA 6 Beta")
    )

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)

@bot.command(name='ping')
async def ping(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! `{latency}ms`")

@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! 👋")

@bot.command(name='info')
async def info(ctx):
    embed = discord.Embed(
        title="Bot Information",
        color=0x5865F2,
        timestamp=ctx.message.created_at
    )
    embed.add_field(name="Latency", value=f"{round(bot.latency*1000)} ms", inline=True)
    embed.add_field(name="Servers", value=str(len(bot.guilds)), inline=True)
    embed.set_footer(text=f"Requested by {ctx.author}")
    
    await ctx.send(embed=embed)

async def main():
    keep_alive()
    async with bot:
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
