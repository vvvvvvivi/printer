# Printer

Auto publish bot for Discord.

Public instance is available at <https://discord.com/oauth2/authorize?client_id=775831907790225490&permissions=76800&scope=bot>.

## Running

```sh
python -m venv venv
source venv/bin/activate
pip install -Ur requirements.txt
DISCORD_TOKEN=[token] python bot.py
```

## Help

This bot has no commands. However, it does respond to bare pings with a small overview about the bot.

### How to prevent auto publishing for some channels?

Revoke the 'Manage Messages' permission from this bot in that channel's permission overrides.

### How do I prevent some messages from being published?

Include `[no-publish]` anywhere in your message.

### How do I prevent user messages from being published?

Give the bot 'Manage Webhooks' permission in that channel.
