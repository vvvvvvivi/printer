import os

import discord
import dotenv

dotenv.load_dotenv()

client = discord.AutoShardedClient(
    intents=discord.Intents(guilds=True, guild_messages=True),
    member_cache_flags=discord.MemberCacheFlags.none(),
    max_messages=0,
    activity=discord.Activity(type=discord.ActivityType.watching, name="announcements"),
)


@client.event
async def on_message(message: discord.Message):
    if message.channel.type != discord.ChannelType.news:
        if message.content in {f"<@!{client.user.id}>", f"<@{client.user.id}>"}:
            app_info = await client.application_info()

            embed = discord.Embed(
                title="Printer",
                description="Auto publish bot for Discord.",
            )
            embed.add_field(
                name="Bot Owner",
                value=f"[{app_info.owner}](https://discord.com/users/{app_info.owner.id})",
                inline=True,
            )
            embed.add_field(
                name="Invite Link",
                value=f"https://discord.com/api/oauth2/authorize?client_id={app_info.id}&permissions=76800&scope=bot",
                inline=True,
            )
            embed.add_field(
                name="Help",
                value="\n".join(
                    [
                        "**How to prevent auto publishing for some channels?**",
                        "Revoke the 'Manage Messages' permission from this bot in that channel's permission overrides.",
                        "",
                        "**How do I prevent some messages from being published?**",
                        "Include `[no-publish]` anywhere in your message.",
                        "",
                        "**How do I prevent user messages from being published?**",
                        "Give the bot 'manage webhooks' permission in that channel.",
                    ]
                ),
                inline=False,
            )

            if message.guild:
                channels = []
                for channel in message.guild.channels:
                    if channel.type != discord.ChannelType.news:
                        continue

                    perms = channel.permissions_for(message.guild.me)

                    missing_perms = []
                    for perm in (
                        "read_message_history",
                        "send_messages",
                        "manage_messages",
                    ):
                        if not getattr(perms, perm):
                            missing_perms.append(perm.replace("_", " "))

                    if missing_perms:
                        channels.append(
                            f"{channel.mention}: missing perms ({', '.join(missing_perms)})"
                        )
                    elif perms.manage_webhooks:
                        channels.append(f"{channel.mention}: bot only")
                    else:
                        channels.append(f"{channel.mention}: active")

                embed.add_field(
                    name="Channels",
                    value="\n".join(channels)
                    if channels
                    else "This server does not have any announcement channels.",
                    inline=False,
                )

            await message.channel.send(embed=embed)

        return

    perms = message.channel.permissions_for(message.guild.me)

    if (
        not perms.read_message_history
        or not perms.send_messages
        or not perms.manage_messages
    ):
        return

    if not message.author.bot and perms.manage_webhooks:
        return

    if "[no-publish]" in message.content:
        return

    await message.publish()


if __name__ == "__main__":
    client.run(os.getenv("DISCORD_TOKEN"))
