# Discord-User-App
script to replace your own messages with an App version of yourself

# Discord Forward Bot

A private Discord bot for personal or small servers.  
It allows authorized users to send **clean messages**: the bot instantly deletes the original message and resends it via a webhook using the user's exact display name, avatar, and content (including multiple attachments). The result looks like a completely normal message with no bot trace.

Perfect for keeping chat tidy or private utility use in servers you control.

**Important Warning**  
This bot deletes messages and uses webhooks to mirror user messages.  
Use **only** in servers where **all members consent** and you are the admin/owner.  
Discord's Terms of Service prohibit deceptive automation or impersonation that could harm others. Misuse (e.g., evading moderation, harassment) may result in your bot or account being restricted/banned. Deploy responsibly.

## Features

- Owner-only authorization system (`!adduser`)
- Per-user toggle (`!on` / `!off`)
- Supports text + multiple attachments
- Authorized users saved permanently (`authorized_users.json`)
- Automatic webhook creation/reuse
- Clean error messages and console logging

## Setup & Usage Guide

**Step 1: Create Your Discord Bot**  
1. Go to the Discord Developer Portal: https://discord.com/developers/applications  
2. Click "New Application" → give it a name (e.g., "ForwardBot") → Create  
3. In the left menu, go to "Bot" → click "Add Bot" → Confirm  
4. Under "Token", click "Copy" → save this somewhere safe (this is your BOT_TOKEN)  
5. Scroll down to "Privileged Gateway Intents" and enable these three:  
   - Presence Intent  
   - Server Members Intent  
   - Message Content Intent (required for reading messages)

**Step 2: Invite the Bot to Your Server**  
1. In the Developer Portal, go to "OAuth2" → "URL Generator"  
2. Under "Scopes", check "bot"  
3. Under "Bot Permissions", check these exact permissions:  
   - View Channels  
   - Send Messages  
   - Manage Webhooks  
   - Manage Messages  
   - Read Message History  
   - Attach Files  
4. Scroll down → copy the generated URL  
5. Paste the URL in your browser → select your server → authorize the bot

**Step 3: Download and Prepare the Code**  
1. Clone or download this repository:  

   git clone https://github.com/evangelions/Discord-User-App
   cd discord-forward-bot

3. Install required packages:  

   pip install -r requirements.txt

**Step 4: Configure Your Secrets and Owner ID**  
1. Create the `.env` file:  

   cp .env.example .env

2. Open `.env` in a text editor and replace the placeholder with your bot token:  

   BOT_TOKEN=your_actual_bot_token_here

3. Open `main.py` in a text editor and find this line:  
```python
AUTHORIZED_OWNER_ID = 123456789012345678  # ← CHANGE THIS TO YOUR USER ID
```


Replace the number with your own Discord user ID:  In Discord: Settings → Advanced → Enable Developer Mode  
Right-click your own username → Copy User ID  
Paste that number here and save the file

## Step 5: Run the Bot**

In your terminal, run:  

python main.py

You should see:  

Bot is ready! Logged in as YourBotName

The bot is now online!

## Step 6: Verify Permissions**

In your server, ensure the bot's role has: Manage Webhooks, Manage Messages, Send Messages, Attach Files, Read Message History, and View Channels  
The bot will automatically create a webhook named "ForwardBot" in each channel when first needed

## How to Use the Bot**

(Command Prefix: !) For Any Authorized User:  !on → Turns forwarding ON (bot replies: "Bot is now ON for you!")  
!off → Turns forwarding OFF (bot replies: "Bot is now OFF for you!")

After using !on, every message you send that does not start with ! will be instantly deleted and resent as a clean message (with your name, avatar, and attachments). as an App
For the Owner Only:  !adduser <user_id> → Adds a new user

Example:  

!adduser 987654321098765432

(Get their user ID: Developer Mode → right-click their name → Copy User ID)
The bot will confirm the user was added. Added users are saved permanently.

Customization (Optional)
Change the command prefix by editing this line in main.py:
```
bot = commands.Bot(command_prefix='!', intents=intents)
```

Replace '!' with your preferred prefix (e.g., '.', '~', etc..). 

## Troubleshooting

Bot not responding? → Check console errors, verify Message Content Intent and token  
Permission errors? → Double-check bot role/channel permissions  
Messages not forwarding? → Confirm you used command and are authorized  
Attachments failing? → Ensure "Attach Files" permission is enabled

Enjoy!
