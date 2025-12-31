import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json
import io

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables. Please set it in your .env file.")

# File to persist authorized users across restarts
USERS_FILE = "authorized_users.json"

# Replace this with your own Discord user ID (the bot owner)
AUTHORIZED_OWNER_ID = 123456789012345678  # ← CHANGE THIS TO YOUR USER ID

# Initial authorized users list (only the owner at start)
AUTHORIZED_USER_IDS = [AUTHORIZED_OWNER_ID]

def load_authorized_users():
    global AUTHORIZED_USER_IDS
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                data = json.load(f)
                AUTHORIZED_USER_IDS = data.get("users", [AUTHORIZED_OWNER_ID])
        except Exception as e:
            print(f"Failed to load authorized users: {e}")

def save_authorized_users():
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump({"users": AUTHORIZED_USER_IDS}, f)
    except Exception as e:
        print(f"Failed to save authorized users: {e}")

load_authorized_users()

intents = discord.Intents.default()
intents.message_content = True
intents.guilds = True
intents.messages = True

bot = commands.Bot(command_prefix='!', intents=intents)

# Per-user activation state (resets on bot restart)
bot_active = {}

@bot.event
async def on_ready():
    print(f'Bot is ready! Logged in as {bot.user}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Error: Missing required argument.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Error: Invalid argument.")
    else:
        await ctx.send(f"An error occurred: {str(error)}")
    print(f"Command error: {error}")

@bot.command(name='on')
async def activate_bot(ctx):
    user_id = ctx.author.id
    if user_id in bot_active and bot_active[user_id]:
        await ctx.send("Bot is already ON for you.")
        return
    bot_active[user_id] = True
    await ctx.send("Bot is now ON for you!")

@bot.command(name='off')
async def deactivate_bot(ctx):
    user_id = ctx.author.id
    if user_id not in bot_active or not bot_active[user_id]:
        await ctx.send("Bot is already OFF for you.")
        return
    bot_active[user_id] = False
    await ctx.send("Bot is now OFF for you!")

@bot.command(name='adduser')
async def add_user(ctx, user_id: int):
    if ctx.author.id != AUTHORIZED_OWNER_ID:
        await ctx.send("You are not authorized to use this command.")
        return
    if user_id not in AUTHORIZED_USER_IDS:
        AUTHORIZED_USER_IDS.append(user_id)
        save_authorized_users()
        await ctx.send(f"User <@{user_id}> has been added to authorized users.")
    else:
        await ctx.send(f"User <@{user_id}> is already authorized.")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    await bot.process_commands(message)

    user_id = message.author.id

    if (user_id in AUTHORIZED_USER_IDS and
        user_id in bot_active and
        bot_active[user_id] and
        not message.content.startswith(bot.command_prefix)):

        try:
            webhooks = await message.channel.webhooks()
            webhook = discord.utils.get(webhooks, name="ForwardBot")
            if webhook is None:
                webhook = await message.channel.create_webhook(name="ForwardBot")
                print(f"Created webhook in #{message.channel.name}")

            files = []
            if message.attachments:
                for attachment in message.attachments:
                    file_data = await attachment.read()
                    files.append(discord.File(fp=io.BytesIO(file_data), filename=attachment.filename))

            send_kwargs = {
                "content": message.content or " ",
                "username": message.author.display_name,
                "avatar_url": message.author.avatar.url if message.author.avatar else None,
                "wait": True
            }
            if files:
                send_kwargs["files"] = files

            await webhook.send(**send_kwargs)
            await message.delete()
            print(f"Forwarded message from {message.author} in #{message.channel.name}")

        except discord.Forbidden:
            await message.channel.send("Error: Bot missing permissions (Manage Webhooks/Manage Messages).")
        except discord.HTTPException as e:
            await message.channel.send("Error: Discord API issue (rate limit, etc.).")
            print(f"HTTP error: {e}")
        except Exception as e:
            await message.channel.send("An unexpected error occurred.")
            print(f"Unexpected error: {type(e).__name__}: {e}")

bot.run(BOT_TOKEN)
