import asyncio
import json
import threading
from datetime import datetime, timedelta, date

import discord
import schedule
from discord import Webhook, RequestsWebhookAdapter
from discord.ext import commands
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from redminelib import Redmine

config = json.load(open("./config.json"))
TOKEN = config["token"]
URL = config["url"]
KEY = config["key"]
VALUE = config["value"]
TIME = config["time"]

hook = Webhook.from_url(config["hook"], adapter=RequestsWebhookAdapter())
redmine = Redmine('https://kore.koders.in/', key='16bc261bac19a91f17fe1bcc8edf79aba43d99a7')

intents = discord.Intents.default()
intents.presences = True
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.event
async def on_ready():
    print('We have logged in as {0.user}'.format(bot))
    data = await main()
    attendance = get_data(data)
    attendance = GSTtoIST(attendance)
    logs = {}
    working_hours = {}
    for user in attendance:
        logs[user] = {}
        working_hours[user] = {}
        for log in attendance[user]:
            try:
                if log['clock_in'] is None:
                    raise Exception
                earliest = min(log['clock_in'], logs[user][log['date']][0])
                latest = max(log['clock_out'], logs[user][log['date']][1])
                if latest > earliest:
                    logs[user].update({log['date']: [earliest, latest]})
                    working_hours[user].update({log['date']: latest - earliest})
            except:
                if log['clock_out'] > log['clock_in']:
                    logs[user].update({log['date']: [log['clock_in'], log['clock_out']]})
                    working_hours[user].update({log['date']: log['clock_out'] - log['clock_in']})
    threading.Thread(target=trigger, args=(working_hours,)).start()


async def main():
    headers = {KEY: "Bearer " + VALUE}
    transport = AIOHTTPTransport(url=URL, headers=headers)
    async with Client(transport=transport, fetch_schema_from_transport=True) as session:
        query = gql(
            """
                query MyQuery {
                    attendance {
                        id
                        date
                        user_id
                        clock_in
                        clock_out
                    }
                }
            """
        )
        try:
            result = await session.execute(query)
            return result
        except Exception as exception:
            print(exception)
            return False


def get_data(dataset):
    users = {}
    for user in dataset["attendance"]:
        try:
            users[user["user_id"]] += [
                {"date": user["date"], "clock_in": user["clock_in"], "clock_out": user["clock_out"]}]
        except:
            users[user["user_id"]] = []
    return users


def GSTtoIST(attendance_data):
    GMT = timedelta(hours=5, minutes=30)
    time_format = "%H:%M:%S"
    date_format = "%Y-%m-%d"
    for user in attendance_data:
        for log in attendance_data[user]:
            log['date'] = datetime.strptime(log['date'], date_format).date()
            if log['clock_in'] is not None:
                dt = datetime.strptime(log['clock_in'], time_format)
                td = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
                log['clock_in'] = td + GMT
            if log['clock_out'] is not None:
                dt = datetime.strptime(log['clock_out'], time_format)
                td = timedelta(hours=dt.hour, minutes=dt.minute, seconds=dt.second)
                log['clock_out'] = td + GMT
            elif log['clock_out'] is None:
                log['clock_out'] = timedelta(hours=18)
    return attendance_data


def convert_time(samey):
    samey = samey.total_seconds()
    hours = samey // 3600
    minutes = (samey % 3600) // 60
    return f"{str(int(hours))} hours, {str(int(minutes))} minutes"


def get_results(daily_hours):
    week = [date.today() - timedelta(ago) for ago in range(5, 0, -1)]
    weekly_hours = {}
    user_week = {}
    for user in daily_hours:
        weekly_hours[user] = timedelta()
        user_week[user] = {}
        for day in daily_hours[user]:
            if day in week:
                weekly_hours[user] += daily_hours[user][day]
                user_week[user].update({day.strftime('%A'): daily_hours[user][day]})
    weekly_hours = {user: total_hours for user, total_hours in weekly_hours.items() if total_hours != timedelta()}
    user_week = {user: user_week[user] for user in user_week if bool(user_week[user])}
    min_hours, max_hours = min(weekly_hours.values()), max(weekly_hours.values())
    min_person = []
    max_person = []
    for person in weekly_hours:
        if weekly_hours[person] == min_hours:
            min_person.append(str(person))
        elif weekly_hours[person] == max_hours:
            max_person.append(str(person))
    max_hours, min_hours = convert_time(max_hours), convert_time(min_hours)
    min_user = [min_person, min_hours]
    max_user = [max_person, max_hours]
    asyncio.run(send_embed(user_week, weekly_hours, min_user, max_user))


async def send_embed(user_week, weekly_hours, min_user, max_user):
    week = [(date.today() - timedelta(ago)).strftime('%A') for ago in range(5, 0, -1)]
    for user in user_week:
        overall = ""
        for day in week:
            try:
                overall += f"**{str(day)}**: {convert_time(user_week[user][day])}\n"
            except:
                overall += f"**{str(day)}**: Absent\n"
        embed = discord.Embed()
        try:
            person = redmine.user.get(user)
            user_name = f"{person['firstname']} {person['lastname']}"
            user_did = int(person['custom_fields'][0]['value'])
            embed.set_author(name=user_name, icon_url=bot.get_user(int(user_did)).avatar_url)
        except:
            embed.set_author(name=str(user))
        embed.description = f"{overall}\n**Total hours:** {convert_time(weekly_hours[user])}"
        embed.color = 43408
        hook.send(embed=embed)
    minimum_attendance = ""
    maximum_attendance = ""
    for user in min_user[0]:
        person = redmine.user.get(int(user))
        minimum_attendance += f"{person['firstname']} {person['lastname']}: {min_user[1]}\n"
    for user in max_user[0]:
        person = redmine.user.get(int(user))
        maximum_attendance += f"{person['firstname']} {person['lastname']}: {max_user[1]}\n"
    embed = discord.Embed()
    embed.title = "Attendance Record"
    embed.add_field(name="Minimum attendance", value=minimum_attendance, inline=False)
    embed.add_field(name="Maximum attendance", value=maximum_attendance, inline=False)
    embed.set_footer(text="Koders")
    file = discord.File("src/logo.png")
    embed.set_thumbnail(url="attachment://logo.png")
    embed.timestamp = datetime.utcnow()
    embed.color = 43408
    hook.send(file=file, embed=embed)


def trigger(working_hours):
    schedule.every().monday.at(TIME).do(get_results, working_hours)
    # schedule.every(TIME).seconds.do(get_results, working_hours)
    while True:
        schedule.run_pending()


bot.run(TOKEN)
