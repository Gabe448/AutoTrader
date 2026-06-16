import os

import nextcord
from nextcord.ext import commands

# Bot setup
intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration - CHANGE THESE
YOUR_USER_ID = 1511597709834977320
TRIGGER_ROLE_ID = 1513925126033379638
DESTINATION_CHANNEL_ID = 1506136302872166480

# Second forwarding rule
USER_ID_2 = 973341703597617185
TRIGGER_ROLE_ID_2 = 1493346507158716458
DESTINATION_CHANNEL_ID_2 = 1458676110928904223

FORWARDING_RULES = [
    {
        "name": "rule 1",
        "user_id": YOUR_USER_ID,
        "trigger_role_id": TRIGGER_ROLE_ID,
        "destination_channel_id": DESTINATION_CHANNEL_ID,
    },
    {
        "name": "rule 2",
        "user_id": USER_ID_2,
        "trigger_role_id": TRIGGER_ROLE_ID_2,
        "destination_channel_id": DESTINATION_CHANNEL_ID_2,
    },
]


@bot.event
async def on_ready():
    print(f"{bot.user} has connected to Discord!")
    for rule in FORWARDING_RULES:
        print(
            f"Monitoring {rule['name']}: "
            f"user={rule['user_id']} "
            f"trigger_role={rule['trigger_role_id']} "
            f"destination={rule['destination_channel_id']}"
        )


async def forward_message(message, rule):
    destination_channel = bot.get_channel(rule["destination_channel_id"])
    if not destination_channel:
        print(
            f"Error: Could not find destination channel "
            f"{rule['destination_channel_id']} for {rule['name']}"
        )
        return

    clean_content = message.content
    for role in message.role_mentions:
        clean_content = clean_content.replace(f"<@&{role.id}>", "").strip()

    image_url = None
    for attachment in message.attachments:
        if attachment.content_type and attachment.content_type.startswith("image/"):
            image_url = attachment.url
            break

    embed = nextcord.Embed(
        description=f"# {clean_content}",
        color=0x5865F2,
        timestamp=message.created_at,
    )
    embed.set_author(
        name=message.author.name,
        icon_url=message.author.display_avatar.url,
    )

    if image_url:
        embed.set_image(url=image_url)

    await destination_channel.send(embed=embed)
    await message.add_reaction("✅")

    print(
        f"Forwarded message from {message.author.name} "
        f"to {destination_channel.name} via {rule['name']}"
    )


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    try:
        for rule in FORWARDING_RULES:
            if message.author.id != rule["user_id"]:
                continue

            if not any(
                role.id == rule["trigger_role_id"] for role in message.role_mentions
            ):
                continue

            await forward_message(message, rule)
            break

    except Exception as error:
        print(f"Error forwarding message: {error}")
        try:
            await message.add_reaction("❌")
        except Exception:
            pass


if __name__ == "__main__":
    token = os.environ.get("DISCORD_BOT_TOKEN")
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN not set!")
    else:
        bot.run(token)
