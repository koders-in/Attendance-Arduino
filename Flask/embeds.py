from discord_webhook import DiscordWebhook, DiscordEmbed
from redmine import get_user_data
import os

WEBHOOK_URL = os.getenv('WEBHOOK_URL')


def create_webhook(user_id, color):
    username, position, opened_issues, total_issues, hours, thumbnail_url = get_user_data(user_id)
    issues = str(opened_issues) + "/" + str(total_issues)
    embed = DiscordEmbed(title="Attendance")
    embed.add_embed_field(name="User", value=username, inline=False)
    embed.add_embed_field(name="Position", value=position, inline=False)
    embed.add_embed_field(name="Issues", value=issues)
    embed.add_embed_field(name="SpentTime", value=str(hours))
    if color == 'green':
        embed.set_color('00ff85')
    else:
        embed.set_color('ff0000')
    embed.set_thumbnail(url=thumbnail_url)
    embed.set_footer(text="Marked at ")
    embed.set_timestamp()
    return embed


def send_webhook(user_id, color):
    webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True)
    embed = create_webhook(user_id, color)
    webhook.add_embed(embed)
    resp = webhook.execute()
    print(resp)
