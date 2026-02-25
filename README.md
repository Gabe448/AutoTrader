# Discord Message Forwarder Bot

Automatically forwards your messages to another server when you ping a specific role.

## Features

- 🎯 Monitors YOUR messages only
- 📨 Forwards when you ping a specific role
- 🖼️ Includes images and attachments
- ✅ Reacts with checkmark to confirm forwarding
- 🔗 Includes jump link to original message

## Setup

### 1. Get Your IDs

**Your User ID:**
1. Enable Developer Mode: Settings → Advanced → Developer Mode
2. Right-click your username → Copy User ID

**Role ID (the role you'll ping to trigger forwarding):**
1. Go to Server Settings → Roles
2. Right-click the role → Copy Role ID

**Destination Channel ID (where messages will be forwarded):**
1. Right-click the destination channel → Copy Channel ID

### 2. Configure bot.py

Open `bot.py` and change these lines:

```python
YOUR_USER_ID = 123456789012345678  # Your Discord user ID
TRIGGER_ROLE_ID = 123456789012345678  # The role ID that triggers forwarding
DESTINATION_CHANNEL_ID = 123456789012345678  # Where to forward messages
```

Replace with your actual IDs.

### 3. Create Discord Bot

1. Go to https://discord.com/developers/applications
2. New Application → Name it "Message Forwarder"
3. Bot tab → Add Bot
4. Enable these Intents:
   - ✅ MESSAGE CONTENT INTENT
   - ✅ SERVER MEMBERS INTENT (optional)
5. Copy Bot Token
6. OAuth2 → URL Generator:
   - Scope: `bot`
   - Permissions: `Read Messages`, `Send Messages`, `Add Reactions`, `Embed Links`
7. Invite bot to BOTH servers (source and destination)

### 4. Deploy to Railway

1. Create GitHub repo and upload these files
2. Go to Railway → New Project → Deploy from GitHub
3. Add environment variable:
   - Name: `DISCORD_BOT_TOKEN`
   - Value: Your bot token
4. Deploy!

## Usage

In any channel where the bot can see your messages:

```
Hey @RoleName check this out!
```

If you ping the configured role, the message will be:
- Forwarded to the destination channel
- Marked with ✅ reaction
- Shown in an embed with server/channel info

## Example

**You send:**
```
@Alerts Important trade setup on SPY!
[chart image attached]
```

**Bot forwards to destination channel:**
```
📨 Forwarded Message
From: YourName
Server: Trading Server
Channel: #alerts
[Your message and image]
[Jump to original]
```

## Notes

- Bot must be in BOTH servers (source and destination)
- Bot needs permission to read messages and add reactions
- Only YOUR messages trigger forwarding
- Works across different servers!
