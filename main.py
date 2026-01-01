import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import io

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Files for persistence
USERS_FILE = "authorized_users.json"
CONFIG_FILE = "bot_config.json"

# === IMPORTANT: CHANGE THIS TO YOUR OWN DISCORD USER ID ===
# Replace this with your personal Discord user ID after setup
AUTHORIZED_OWNER_ID = 123456789012345678  # ← CHANGE THIS!

# Initial authorized users list (will only contain the owner at first)
AUTHORIZED_USER_IDS = [AUTHORIZED_OWNER_ID]

# Default prefix if no config exists
DEFAULT_PREFIX = "!"

def load_authorized_users():
    """Load authorized users from file, ensuring owner is always included"""
    global AUTHORIZED_USER_IDS
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                data = json.load(f)
                loaded_users = data.get("users", [])
                # Ensure owner is always authorized, even if removed from file
                if AUTHORIZED_OWNER_ID not in loaded_users:
                    loaded_users.append(AUTHORIZED_OWNER_ID)
                AUTHORIZED_USER_IDS = loaded_users
        except Exception as e:
            print(f"Failed to load authorized users: {e}")
            AUTHORIZED_USER_IDS = [AUTHORIZED_OWNER_ID]

def save_authorized_users():
    """Save current authorized users to file"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump({"users": AUTHORIZED_USER_IDS}, f)
    except Exception as e:
        print(f"Failed to save authorized users: {e}")

def get_prefix(bot, message):
    """Dynamically load prefix from config file"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                return config.get("prefix", DEFAULT_PREFIX)
        except Exception:
            pass
    return DEFAULT_PREFIX

def save_prefix(new_prefix):
    """Save new prefix to config file"""
    try:
        with open(CONFIG_FILE, 'w') as f:
            json.dump({"prefix": new_prefix}, f)
    except Exception as e:
        print(f"Failed to save prefix: {e}")

# Load authorized users on startup
load_authorized_users()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

# Use dynamic prefix
bot = commands.Bot(command_prefix=get_prefix, intents=intents)

# Remove default help command
bot.remove_command("help")

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')
    current_prefix = get_prefix(bot, None)
    print(f"Current prefix: {current_prefix}")

@bot.command(name='setprefix')
async def set_prefix(ctx, new_prefix: str):
    """Owner-only: Change the bot's command prefix"""
    if ctx.author.id != AUTHORIZED_OWNER_ID:
        await ctx.send("❌ Only the bot owner can use this command.")
        return

    if len(new_prefix) > 10:
        await ctx.send("❌ Prefix too long (max 10 characters).")
        return

    if not new_prefix.strip():
        await ctx.send("❌ Prefix cannot be empty or just whitespace.")
        return

    save_prefix(new_prefix.strip())
    bot.command_prefix = new_prefix.strip()  # Immediate update

    await ctx.send(f"✅ Bot prefix changed to `{new_prefix.strip()}`\n"
                   f"This change is permanent and survives restarts.")

@bot.command(name='help')
async def help_command(ctx):
    user_id = ctx.author.id
    embed = discord.Embed(title="Bot Commands", description="Available commands:", color=0x00ff00)
    prefix = bot.command_prefix if isinstance(bot.command_prefix, str) else bot.command_prefix(bot, ctx.message)

    if user_id in AUTHORIZED_USER_IDS:
        embed.add_field(name=f"{prefix}on", value="Turn message forwarding ON", inline=False)
        embed.add_field(name=f"{prefix}off", value="Turn message forwarding OFF", inline=False)
        embed.add_field(name=f"{prefix}status", value="Check your current status", inline=False)
        embed.add_field(name=f"{prefix}help", value="Show this help message", inline=False)

    if user_id == AUTHORIZED_OWNER_ID:
        embed.add_field(name=f"{prefix}adduser <user_id>", value="Authorize a new user", inline=False)
        embed.add_field(name=f"{prefix}remove <user_id>", value="Remove a user from authorized list", inline=False)
        embed.add_field(name=f"{prefix}listusers", value="List all authorized users", inline=False)
        embed.add_field(name=f"{prefix}setprefix <prefix>", value="Change command prefix (owner only)", inline=False)

    if embed.fields:
        await ctx.send(embed=embed)
    else:
        await ctx.send("You don't have access to any commands.")

@bot.command(name='status')
async def bot_status(ctx):
    if ctx.author.id not in AUTHORIZED_USER_IDS:
        return
    status = "ON" if bot_active.get(ctx.author.id, False) else "OFF"
    await ctx.send(f"The bot is currently **{status}** for you.")

@bot.command(name='listusers')
async def list_users(ctx):
    if ctx.author.id != AUTHORIZED_OWNER_ID:
        await ctx.send("You are not authorized to use this command.")
        return

    if len(AUTHORIZED_USER_IDS) == 1:
        await ctx.send("**Authorized users:**\nOnly you (the owner)")
    else:
        user_list = "\n".join(f"<@{uid}> (ID: {uid})" for uid in AUTHORIZED_USER_IDS if uid != AUTHORIZED_OWNER_ID)
        await ctx.send(f"**Authorized users:**\n<@{AUTHORIZED_OWNER_ID}> (owner)\n{user_list}")

@bot.command(name='on')
async def activate_bot(ctx):
    user_id = ctx.author.id
    if user_id not in AUTHORIZED_USER_IDS:
        return
    if bot_active.get(user_id, False):
        await ctx.send("Bot is already ON for you.")
        return
    bot_active[user_id] = True
    await ctx.send("Bot is now ON for you!")

@bot.command(name='off')
async def deactivate_bot(ctx):
    user_id = ctx.author.id
    if user_id not in AUTHORIZED_USER_IDS:
        return
    if not bot_active.get(user_id, False):
        await ctx.send("Bot is already OFF for you.")
        return
    bot_active[user_id] = False
    await ctx.send("Bot is now OFF for you!")

@bot.command(name='adduser')
async def add_user(ctx, user_id: int):
    if ctx.author.id != AUTHORIZED_OWNER_ID:
        await ctx.send("You are not authorized to use this command.")
        return
    if user_id in AUTHORIZED_USER_IDS:
        await ctx.send(f"User <@{user_id}> is already authorized.")
    else:
        AUTHORIZED_USER_IDS.append(user_id)
        save_authorized_users()
        await ctx.send(f"User <@{user_id}> has been added to authorized users.")

@bot.command(name='remove')
async def remove_user(ctx, user_id: int):
    if ctx.author.id != AUTHORIZED_OWNER_ID:
        await ctx.send("You are not authorized to use this command.")
        return
    if user_id == AUTHORIZED_OWNER_ID:
        await ctx.send("You cannot remove yourself (the owner).")
        return
    if user_id in AUTHORIZED_USER_IDS:
        AUTHORIZED_USER_IDS.remove(user_id)
        save_authorized_users()
        if user_id in bot_active:
            del bot_active[user_id]
        await ctx.send(f"User <@{user_id}> has been removed.")
    else:
        await ctx.send(f"User <@{user_id}> was not in the authorized list.")

# In-memory per-user state
bot_active = {}

@bot.event
async def on_message(message):
    if message.author == bot.user or message.author.bot:
        return

    await bot.process_commands(message)

    user_id = message.author.id
    current_prefix = bot.command_prefix if isinstance(bot.command_prefix, str) else bot.command_prefix(bot, message)

    if (user_id in AUTHORIZED_USER_IDS
        and bot_active.get(user_id, False)
        and not message.content.startswith(current_prefix)):

        try:
            webhooks = await message.channel.webhooks()
            webhook = discord.utils.get(webhooks, name="ForwardBot")
            if webhook is None:
                webhook = await message.channel.create_webhook(name="ForwardBot")
                print(f"Created webhook in #{message.channel.name}")

            files = []
            for attachment in message.attachments:
                file_data = await attachment.read()
                files.append(discord.File(fp=io.BytesIO(file_data), filename=attachment.filename))

            content = message.content or ( "‎" if (message.embeds or message.stickers or message.attachments) else "" )

            await webhook.send(
                content=content or "‎",
                username=message.author.display_name,
                avatar_url=message.author.avatar.url if message.author.avatar else message.author.default_avatar.url,
                files=files or None,
                wait=True
            )
            await message.delete()
            print(f"Forwarded message from {message.author} in #{message.channel.name}")

        except discord.Forbidden:
            await message.channel.send("Error: Missing permissions (Manage Webhooks/Manage Messages).")
        except discord.HTTPException as e:
            await message.channel.send("Error: Discord API issue (possibly rate-limited).")
            print(f"HTTPException: {e}")
        except Exception as e:
            await message.channel.send("An unexpected error occurred.")
            print(f"Error processing message from {user_id}: {e}")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in .env file!")

bot.run(BOT_TOKEN)
