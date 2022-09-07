from slack_webhook import Slack
from redmine import get_user_data
import os

WEBHOOK_URL = os.getenv('WEBHOOK_URL')


def send_webhook(user_id, color):
    username, position, opened_issues, total_issues, hours, thumbnail_url = get_user_data(user_id)
    slack = Slack(url=WEBHOOK_URL)
    slack.post(text="",
   
    blocks=[{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": f"*User:*\n{username}".format(username=username)
				},
				{
					"type": "mrkdwn",
					"text": f"*Position:*\n{position}".format(position=position)
				},
				{
					"type": "mrkdwn",
					"text": f"*Issues:*\n{opened_issues}/{total_issues}".format(opened_issues=opened_issues,total_issues=total_issues)
				},
				{
					"type": "mrkdwn",
					"text": f"*Spent Time:*\n{hours}.".format(hours=hours)
				}
			],
            "accessory": {
				"type": "image",
				"image_url": thumbnail_url,
				"alt_text": "computer thumbnail"
			}
		},
        {
			"type": "actions",
			"elements": [
				{
					"type": "button",
					"text": {
						"type": "plain_text",
			            "text": "View my attendance"
					},
					"style": "primary",
					"url": "https://www.google.com"
				}
			],
      
		},
       ]
)
	


