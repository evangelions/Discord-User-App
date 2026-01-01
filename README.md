# Discord-User-App

Script to replace your own messages with an App version of yourself.
It allows authorized users to send App messages: the bot instantly deletes the original message and resends it via a webhook using the user's exact display name & pfp,
(including multiple attachments). The result looks like a message sent by an "App" version of you.



**Important Warning**  
This bot deletes messages and uses webhooks to mirror user messages.  
Use **only** in servers where **all members consent** and you are the admin/owner.  
Discord's Terms of Service prohibit deceptive automation or impersonation that could harm others. Misuse (e.g., evading moderation, harassment) may result in your bot or account being restricted/banned. use responsibly.

## Features

- Owner-only authorization system (!adduser, !remove, !listusers)
- Owner-only command to change the bot's prefix (!setprefix)
- Per-user toggle (!on / !off)
- Supports text + multiple attachments
- Authorized users saved permanently (authorized_users.json)
- Bot prefix saved permanently (bot_config.json)
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

1. Open `.env` in a text editor and replace the placeholder with your bot token:  

   BOT_TOKEN=your_actual_bot_token_here

2. Open `main.py` in a text editor and find this line:  
```python
AUTHORIZED_OWNER_ID = 123456789012345678  # ← CHANGE THIS TO YOUR USER ID
```


Replace the number with your own Discord user ID:  
In Discord: Settings → Advanced → Enable Developer Mode  
Right-click your own username → Copy User ID  
Paste that number here and save the file


## Step 5: Run the Bot

In your terminal,

run:  python main.py

You should see:  Bot is ready! Logged in as YourBotName

The bot is now online!

## Step 6: Verify Permissions

Ensure the bot's role has these permissions:
- Manage Webhooks
- Manage Messages
- Send Messages
- Attach Files
- Read Message History
- View Channels

The bot will automatically create a webhook named ForwardBot in each channel when needed.



## How to Use the Bot

Default Command Prefix: "!" (changeable by owner with !setprefix)

**For Any Authorized User**

- !on → Turns forwarding ON
- !off → Turns forwarding OFF
- !status → Check your current forwarding status
- !help → Shows all available commands

After !on, any message not starting with the prefix will be instantly deleted and re-sent as a clean "App" message (with your name & pfp)


**Owner-Only Commands**

- !adduser <user_id> → Add a user to the authorized list
- !remove <user_id> → Remove a user from the authorized list
- !listusers → List all authorized users
- !setprefix <new_prefix> → Permanently change the command prefix

Example: !setprefix ? → Commands become ?on, ?help, etc.
Prefix Change persists after restarts.


## Example:  

!adduser 987654321098765432

(Get their user ID: Developer Mode → right-click their name → Copy User ID)
The bot will confirm the user was added. Added users are saved permanently.


## Troubleshooting

- Bot not responding?  Check console errors, verify Message Content Intent and token
- Permission errors?  Double-check bot role and channel overrides
- Messages not forwarding?  Ensure you used !on and are authorized
- Attachments failing?  Confirm "Attach Files" permission is enabled
- Prefix not updating?  Only the owner can use !setprefix


# Enjoy!
