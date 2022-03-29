from discord_webhook import DiscordWebhook, DiscordEmbed

WEBHOOK_URL = "https://discord.com/api/webhooks/958342332313378886/syQp5KZHa2gF583OiSUNOG_E_JYgssupiAyyKs616jmB6F1F6MuBY-0DZ6NILong8dFG"


def get_color(shift):
    if shift == "dawn_in":
        color = "91203"
    return color


def get_shift(shift):
    if shift == "dawn_in":
        color = "91203"
    return color


def create_webhook(username, position, shift, thumbnail_url):
    embed = DiscordEmbed(title="Attendance")
    embed.add_embed_field(name="User", value=username)
    embed.add_embed_field(name="Position", value=position)
    embed.add_embed_field(name="Type", value="Morning check-in")
    embed.set_thumbnail(url=thumbnail_url)
    embed.set_footer(text="Marked at ")
    embed.set_timestamp()

    if shift == "check-in":
        embed.set_color(color="ff0000")
    elif shift == "check-out":
        embed.set_color(color="00ff85")
    return embed


def send_webhook(username, position, shift, thumbnail_url):
    webhook = DiscordWebhook(url=WEBHOOK_URL, rate_limit_retry=True)
    embed = create_webhook(username, position, shift, thumbnail_url)
    webhook.add_embed(embed)
    resp = webhook.execute()
    return resp


def process_webhook_output(resp):
    print(resp)


response = send_webhook("Shalika Sharma", "Graphic UI/UX Intern Level 1", "check-in", "https://i.pinimg.com/originals/19/cf/78/19cf789a8e216dc898043489c16cec00.jpg")
process_webhook_output(response)
