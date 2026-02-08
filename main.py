import discord
from discord.ext import commands
import os
import asyncio
import time

from keep_alive import keep_alive

# Global variable to store start time
start_time = None

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
    global start_time
    start_time = time.time()  # Record exact start time (in seconds since epoch)
    
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

def get_uptime():
    if start_time is None:
        return "Bot is still starting..."
    
    uptime_seconds = int(time.time() - start_time)
    
    days = uptime_seconds // (24 * 3600)
    uptime_seconds %= (24 * 3600)
    hours = uptime_seconds // 3600
    uptime_seconds %= 3600
    minutes = uptime_seconds // 60
    seconds = uptime_seconds % 60
    
    parts = []
    if days > 0:
        parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0:
        parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes > 0:
        parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds > 0 or not parts:  # show seconds if nothing else
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    
    return ", ".join(parts)

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

@bot.command(name='timehosted')
async def timehosted(ctx):
    uptime = get_uptime()
    embed = discord.Embed(
        title="Bot Uptime",
        description=f"I've been online for:\n**{uptime}**",
        color=0x00ff00,  # nice green color
        timestamp=ctx.message.created_at
    )
    embed.set_footer(text=f"Requested by {ctx.author}")
    
    await ctx.send(embed=embed)

async def main():
    keep_alive()
    async with bot:
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
