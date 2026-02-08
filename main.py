import discord
from discord.ext import commands
import random
import os
import asyncio
import time
from collections import deque

from keep_alive import keep_alive

# Prevent double command execution
processed_messages = set()

# Store deleted messages per channel (no limit)
deleted_messages = {}  # channel_id → deque[(content, author, created_at, attachments)]

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
    start_time = time.time()
    
    print("───────────────────────────────────────────────")
    print(f"Logged in as   : {bot.user}")
    print(f"User ID        : {bot.user.id}")
    print(f"Guilds         : {len(bot.guilds)}")
    print("───────────────────────────────────────────────")
    
    await bot.change_presence(
        activity=discord.Game(name="GTA 6 Beta")
    )

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    msg_id = message.id
    if msg_id in processed_messages:
        return
    
    processed_messages.add(msg_id)
    
    if len(processed_messages) > 10000:
        processed_messages.clear()
    
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message: discord.Message):
    if message.author.bot:
        return
    
    channel_id = message.channel.id
    
    if channel_id not in deleted_messages:
        deleted_messages[channel_id] = deque()
    
    content = message.content if message.content else "[No text content]"
    attachments = [att.url for att in message.attachments] if message.attachments else []
    
    deleted_messages[channel_id].appendleft((
        content,
        message.author,
        message.created_at,
        attachments
    ))

def get_uptime():
    if start_time is None:
        return "Bot is still starting..."
    
    uptime_seconds = int(time.time() - start_time)
    days = uptime_seconds // 86400
    uptime_seconds %= 86400
    hours = uptime_seconds // 3600
    uptime_seconds %= 3600
    minutes = uptime_seconds // 60
    seconds = uptime_seconds % 60
    
    parts = []
    if days: parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours: parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
    if minutes: parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
    if seconds or not parts: parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    
    return ", ".join(parts)

# ────────────────────────────────────────────────
# PREFIX COMMANDS
# ────────────────────────────────────────────────

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
        description=f"Online for: **{uptime}**",
        color=0x00ff00,
        timestamp=ctx.message.created_at
    )
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

@bot.command(name='gaymeter')
async def gaymeter(ctx, member: discord.Member = None):
    target = member or ctx.author
    SPECIAL_ID = 1323331952559919235
    percentage = 0 if target.id == SPECIAL_ID else random.randint(0, 100)
    
    result_text = (
        "Fully Straight! 📏" if percentage == 0 else
        "Stay fabulous! ✨" if percentage > 80 else
        "Getting there! 💅" if percentage > 50 else
        "Quite straight! 📏"
    )
    
    embed = discord.Embed(
        title="🌈 Gay Meter",
        color=0xFF5500,
        description=f"**{target.display_name}** → **{percentage}%** Gay 🏳️‍🌈\n\n{result_text}"
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.set_footer(text="Gay Meter")
    await ctx.send(embed=embed)

@bot.command(name='dihmeter')
async def dihmeter(ctx, member: discord.Member = None):
    target = member or ctx.author
    SPECIAL_ID = 1323331952559919235
    
    if target.id == SPECIAL_ID:
        inches = random.randint(15, 20)
    else:
        r = random.random()
        if r < 0.70: inches = random.randint(0, 9)
        elif r < 0.90: inches = random.randint(10, 14)
        elif r < 0.985: inches = random.randint(15, 18)
        elif r < 0.995: inches = 19
        else: inches = 20
    
    result_text = (
        "You have a clih not a dih 😭" if inches == 0 else
        "God-tier monster 🐉🔥" if inches >= 18 else
        "Absolute unit 🏋️‍♂️" if inches >= 15 else
        "Big boy energy 💪" if inches >= 12 else
        "Respectable 📏" if inches >= 8 else
        "Average Joe 🤝" if inches >= 5 else
        "Quite Small 🤏" if inches >= 2 else
        "Small as fuck 🐜"
    )
    
    embed = discord.Embed(
        title="Dih Meter",
        color=0xFF5500,
        description=f"**{target.display_name}** → **{inches}** Inches\n\n{result_text}"
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.set_footer(text="Dih Meter")
    await ctx.send(embed=embed)

@bot.command(name='snipe')
async def snipe(ctx, index: int = 1):
    """Snipe deleted messages: c.snipe, c.snipe 2, c.snipe 3..."""
    channel_id = ctx.channel.id
    
    if channel_id not in deleted_messages or not deleted_messages[channel_id]:
        await ctx.send("No deleted messages to snipe in this channel yet.")
        return
    
    history = deleted_messages[channel_id]
    
    if index < 1 or index > len(history):
        await ctx.send(f"Only {len(history)} sniped message(s) available.")
        return
    
    content, author, timestamp, attachments = history[index - 1]
    
    embed = discord.Embed(
        title="Sniped Message",
        description=content,
        color=0xe74c3c,
        timestamp=timestamp
    )
    embed.set_author(name=f"{author.display_name} ({author})", icon_url=author.display_avatar.url)
    embed.set_footer(text=f"#{index}/{len(history)} • Deleted")
    
    if attachments:
        embed.add_field(name="Attachments", value="\n".join(attachments[:5]), inline=False)
        if attachments and any(attachments[0].lower().endswith(ext) for ext in ('.png','.jpg','.jpeg','.gif','.webp')):
            embed.set_image(url=attachments[0])
    
    await ctx.send(embed=embed)

@bot.command(name='clearsnipe')
async def clearsnipe(ctx):
    """Clear all sniped (deleted) messages history in this channel"""
    channel_id = ctx.channel.id
    
    if channel_id in deleted_messages and deleted_messages[channel_id]:
        count = len(deleted_messages[channel_id])
        deleted_messages[channel_id].clear()
        await ctx.send(f"🗑️ Cleared **{count}** sniped message(s) from this channel.")
    else:
        await ctx.send("No snipe history to clear in this channel.")

# ────────────────────────────────────────────────
# RUN THE BOT
# ────────────────────────────────────────────────

async def main():
    keep_alive()
    async with bot:
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
