import os

import discord

client = discord.AutoShardedClient(
    intents=discord.Intents(guilds=True, guild_messages=True),
    member_cache_flags=discord.MemberCacheFlags.none(),
    max_messages=0,
    activity=discord.Activity(type=discord.ActivityType.watching, name="announcements"),
)


@client.event
async def on_message(message: discord.Message):
    if message.channel.type != discord.ChannelType.news:
        return

    perms = message.channel.permissions_for(message.author)
    if (
        not perms.read_message_history
        or not perms.send_messages
        or not perms.manage_messages
    ):
        return

    await message.publish()


if __name__ == "__main__":
    client.run(os.getenv("DISCORD_TOKEN"))
