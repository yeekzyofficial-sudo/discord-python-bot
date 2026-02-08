import discord
from discord import app_commands
from discord.ext import commands
import random
import os
import asyncio
import time
from collections import deque
from datetime import datetime

from keep_alive import keep_alive

# Track processed IDs to prevent double execution
processed_messages = set()
processed_interactions = set()

# Store deleted messages per channel (no limit)
# channel_id → deque of (content, author, created_at, attachments_urls)
deleted_messages = {}

# Store bot start time for uptime
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
    
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} slash command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    msg_id = message.id
    if msg_id in processed_messages:
        return
    
    processed_messages.add(msg_id)
    
    # Optional cleanup (prevents memory growth forever)
    if len(processed_messages) > 5000:
        processed_messages.clear()
    
    await bot.process_commands(message)

@bot.event
async def on_message_delete(message: discord.Message):
    if message.author.bot:
        return
    
    channel_id = message.channel.id
    
    if channel_id not in deleted_messages:
        deleted_messages[channel_id] = deque()  # no maxlen = unlimited
    
    attachments = [att.url for att in message.attachments] if message.attachments else []
    
    deleted_messages[channel_id].appendleft((
        message.content or "[No text content]",
        message.author,
        message.created_at,
        attachments
    ))

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
    if seconds > 0 or not parts:
        parts.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    
    return ", ".join(parts)

# ────────────────────────────────────────────────
# PREFIX COMMANDS (c.)
# ────────────────────────────────────────────────

@bot.command(name='ping')
async def ping_prefix(ctx):
    latency = round(bot.latency * 1000)
    await ctx.send(f"🏓 Pong! `{latency}ms`")

@bot.command(name='hello')
async def hello_prefix(ctx):
    await ctx.send(f"Hello {ctx.author.mention}! 👋")

@bot.command(name='info')
async def info_prefix(ctx):
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
async def timehosted_prefix(ctx):
    uptime = get_uptime()
    embed = discord.Embed(
        title="Bot Uptime",
        description=f"I've been online for:\n**{uptime}**",
        color=0x00ff00,
        timestamp=ctx.message.created_at
    )
    embed.set_footer(text=f"Requested by {ctx.author}")
    await ctx.send(embed=embed)

@bot.command(name='gaymeter')
async def gaymeter_prefix(ctx, member: discord.Member = None):
    target = member or ctx.author
    SPECIAL_ID = 1323331952559919235
    
    if target.id == SPECIAL_ID:
        percentage = 0
    else:
        percentage = random.randint(0, 100)
    
    if percentage == 0:
        result_text = "Fully Straight! 📏"
    elif percentage > 80:
        result_text = "Stay fabulous! ✨"
    elif percentage > 50:
        result_text = "Getting there! 💅"
    else:
        result_text = "Quite straight! 📏"
    
    embed = discord.Embed(
        title="🌈 Gay Meter",
        color=0xFF5500,
        description=(
            f"Checking the **Gay** percentage for **{target.display_name}**...\n\n"
            f"**Result:**\n"
            f"{percentage}% Gay 🏳️‍🌈\n\n"
            f"{result_text}"
        )
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.set_footer(text="Gay Meter")
    await ctx.send(embed=embed)

@bot.command(name='dihmeter')
async def dihmeter_prefix(ctx, member: discord.Member = None):
    target = member or ctx.author
    SPECIAL_ID = 1323331952559919235
    
    if target.id == SPECIAL_ID:
        inches = random.randint(15, 20)
    else:
        rand = random.random()
        if rand < 0.70:
            inches = random.randint(0, 9)
        elif rand < 0.90:
            inches = random.randint(10, 14)
        elif rand < 0.985:
            inches = random.randint(15, 18)
        elif rand < 0.995:
            inches = 19
        else:
            inches = 20
    
    if inches == 0:
        result_text = "You have a clih not a dih 😭"
    elif inches >= 18:
        result_text = "God-tier monster 🐉🔥"
    elif inches >= 15:
        result_text = "Absolute unit 🏋️‍♂️"
    elif inches >= 12:
        result_text = "Big boy energy 💪"
    elif inches >= 8:
        result_text = "Respectable 📏"
    elif inches >= 5:
        result_text = "Average Joe 🤝"
    elif inches >= 2:
        result_text = "Quite Small 🤏"
    else:
        result_text = "Small as fuck 🐜"
    
    embed = discord.Embed(
        title="Dih Meter",
        color=0xFF5500,
        description=(
            f"Checking the **Dih** Inches for **{target.display_name}**...\n\n"
            f"**Result:**\n"
            f"{inches} Inches\n\n"
            f"{result_text}"
        )
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.set_footer(text="Dih Meter")
    await ctx.send(embed=embed)

@bot.command(name='snipe')
async def snipe(ctx, index: int = 1):
    """Shows recently deleted messages. Use c.snipe 2, c.snipe 3, etc."""
    channel_id = ctx.channel.id
    
    if channel_id not in deleted_messages or not deleted_messages[channel_id]:
        await ctx.send("No recently deleted messages to snipe in this channel.")
        return
    
    history = deleted_messages[channel_id]
    
    if index < 1 or index > len(history):
        await ctx.send(f"Invalid index. Only {len(history)} deleted message(s) available.")
        return
    
    content, author, timestamp, attachments = history[index - 1]
    
    embed = discord.Embed(
        title="Sniped Message",
        description=content,
        color=0xe74c3c,
        timestamp=timestamp
    )
    
    embed.set_author(
        name=f"{author.display_name} ({author})",
        icon_url=author.display_avatar.url
    )
    
    embed.set_footer(text=f"Message {index}/{len(history)} • Deleted")
    
    if attachments:
        embed.add_field(
            name="Attachments",
            value="\n".join(attachments[:5]),
            inline=False
        )
        # Show first image if possible
        if attachments and attachments[0].lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
            embed.set_image(url=attachments[0])
    
    await ctx.send(embed=embed)

# ────────────────────────────────────────────────
# SLASH COMMANDS (/)
# ────────────────────────────────────────────────

@bot.tree.command(name="ping", description="Check the bot's latency")
async def ping_slash(interaction: discord.Interaction):
    latency = round(bot.latency * 1000)
    await interaction.response.send_message(f"🏓 Pong! `{latency}ms`")

@bot.tree.command(name="hello", description="Say hello to the bot")
async def hello_slash(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hello {interaction.user.mention}! 👋")

@bot.tree.command(name="info", description="Show bot information")
async def info_slash(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Bot Information",
        color=0x5865F2,
        timestamp=interaction.created_at
    )
    embed.add_field(name="Latency", value=f"{round(bot.latency*1000)} ms", inline=True)
    embed.add_field(name="Servers", value=str(len(bot.guilds)), inline=True)
    embed.set_footer(text=f"Requested by {interaction.user}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="timehosted", description="Show how long the bot has been online")
async def timehosted_slash(interaction: discord.Interaction):
    uptime = get_uptime()
    embed = discord.Embed(
        title="Bot Uptime",
        description=f"I've been online for:\n**{uptime}**",
        color=0x00ff00,
        timestamp=interaction.created_at
    )
    embed.set_footer(text=f"Requested by {interaction.user}")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="gaymeter", description="Check someone's gay percentage 🌈")
@app_commands.describe(user="The person to check (optional)")
async def gaymeter_slash(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    SPECIAL_ID = 1323331952559919235
    
    if target.id == SPECIAL_ID:
        percentage = 0
    else:
        percentage = random.randint(0, 100)
    
    if percentage == 0:
        result_text = "Fully Straight! 📏"
    elif percentage > 80:
        result_text = "Stay fabulous! ✨"
    elif percentage > 50:
        result_text = "Getting there! 💅"
    else:
        result_text = "Quite straight! 📏"
    
    embed = discord.Embed(
        title="🌈 Gay Meter",
        color=0xFF5500,
        description=(
            f"Checking the **Gay** percentage for **{target.display_name}**...\n\n"
            f"**Result:**\n"
            f"{percentage}% Gay 🏳️‍🌈\n\n"
            f"{result_text}"
        )
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.set_footer(text="Gay Meter")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="dihmeter", description="Check someone's dih size in inches 🍆")
@app_commands.describe(user="The person to check (optional)")
async def dihmeter_slash(interaction: discord.Interaction, user: discord.Member = None):
    target = user or interaction.user
    SPECIAL_ID = 1323331952559919235
    
    if target.id == SPECIAL_ID:
        inches = random.randint(15, 20)
    else:
        rand = random.random()
        if rand < 0.70:
            inches = random.randint(0, 9)
        elif rand < 0.90:
            inches = random.randint(10, 14)
        elif rand < 0.985:
            inches = random.randint(15, 18)
        elif rand < 0.995:
            inches = 19
        else:
            inches = 20
    
    if inches == 0:
        result_text = "You have a clih not a dih 😭"
    elif inches >= 18:
        result_text = "God-tier monster 🐉🔥"
    elif inches >= 15:
        result_text = "Absolute unit 🏋️‍♂️"
    elif inches >= 12:
        result_text = "Big boy energy 💪"
    elif inches >= 8:
        result_text = "Respectable 📏"
    elif inches >= 5:
        result_text = "Average Joe 🤝"
    elif inches >= 2:
        result_text = "Quite Small 🤏"
    else:
        result_text = "Small as fuck 🐜"
    
    embed = discord.Embed(
        title="Dih Meter",
        color=0xFF5500,
        description=(
            f"Checking the **Dih** Inches for **{target.display_name}**...\n\n"
            f"**Result:**\n"
            f"{inches} Inches\n\n"
            f"{result_text}"
        )
    )
    embed.set_thumbnail(url=target.display_avatar.url)
    embed.set_footer(text="Dih Meter")
    await interaction.response.send_message(embed=embed)

# ────────────────────────────────────────────────
# RUN THE BOT
# ────────────────────────────────────────────────

async def main():
    keep_alive()
    async with bot:
        await bot.start(os.getenv("DISCORD_TOKEN"))

if __name__ == "__main__":
    asyncio.run(main())
