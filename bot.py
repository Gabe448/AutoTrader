import nextcord
from nextcord.ext import commands
import os

# Bot setup
intents = nextcord.Intents.default()
intents.messages = True
intents.message_content = True
intents.guilds = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Configuration - CHANGE THESE
YOUR_USER_ID =  973341703597617185 # Your Discord user ID
TRIGGER_ROLE_ID = 1460610412813881425  # The role ID that triggers forwarding
DESTINATION_CHANNEL_ID = 1473364678754177236  # Where to forward messages

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    print(f'Monitoring messages from user ID: {YOUR_USER_ID}')
    print(f'Trigger role ID: {TRIGGER_ROLE_ID}')
    print(f'Forwarding to channel ID: {DESTINATION_CHANNEL_ID}')

@bot.event
async def on_message(message):
    # Ignore bot messages
    if message.author.bot:
        return
    
    # Only process messages from you
    if message.author.id != YOUR_USER_ID:
        return
    
    # Check if the trigger role is mentioned in the message
    if not any(role.id == TRIGGER_ROLE_ID for role in message.role_mentions):
        return
    
    # Get the destination channel
    destination_channel = bot.get_channel(DESTINATION_CHANNEL_ID)
    
    if not destination_channel:
        print(f"Error: Could not find destination channel {DESTINATION_CHANNEL_ID}")
        return
    
    try:
        # Create embed for forwarded message
        embed = nextcord.Embed(
            description=message.content,
            color=0x5865F2,
            timestamp=message.created_at
        )
        
        embed.set_author(
            name=f"{message.author.name}",
            icon_url=message.author.display_avatar.url
        )
        
        embed.add_field(
            name="Original Server",
            value=message.guild.name,
            inline=True
        )
        
        embed.add_field(
            name="Original Channel",
            value=f"#{message.channel.name}",
            inline=True
        )
        
        embed.add_field(
            name="Jump to Message",
            value=f"[Click here]({message.jump_url})",
            inline=False
        )
        
        # Forward attachments if any
        files = []
        if message.attachments:
            for attachment in message.attachments:
                # Download and forward image attachments
                if attachment.content_type and attachment.content_type.startswith('image/'):
                    embed.set_image(url=attachment.url)
                else:
                    # For non-images, include link
                    embed.add_field(
                        name="Attachment",
                        value=f"[{attachment.filename}]({attachment.url})",
                        inline=False
                    )
        
        # Send to destination
        await destination_channel.send(embed=embed)
        
        # Optional: React to original message to confirm forwarding
        await message.add_reaction("✅")
        
        print(f"Forwarded message from {message.author.name} to {destination_channel.name}")
        
    except Exception as e:
        print(f"Error forwarding message: {e}")
        # Optional: React with error emoji
        try:
            await message.add_reaction("❌")
        except:
            pass

# Run bot
if __name__ == '__main__':
    token = os.environ.get('DISCORD_BOT_TOKEN')
    if not token:
        print("ERROR: DISCORD_BOT_TOKEN not set!")
    else:
        bot.run(token)
