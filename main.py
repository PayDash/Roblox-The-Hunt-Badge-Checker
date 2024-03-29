#made at 3 am on a saturday night
import datetime
import json
import requests
import os
from discord_webhook import DiscordWebhook, DiscordEmbed

with open('config.json', 'r') as f:
    config = json.load(f)
    webhook_url = config['webhook']
    
with open("ids.json", "r") as f:
    Badge = json.load(f)

print("Input UserID below:")
UserID = str(input("\n"))

if os.name == "posix":
    ClearConsole = "clear"
elif os.name == "nt":
    ClearConsole = "cls"

os.system(ClearConsole)

if not UserID.isnumeric():
    raise Exception("Invalid UserID")

BadgesUrl = f"https://badges.roblox.com/v1/users/{UserID}/badges?limit=100&sortOrder=Asc"
UsersUrl = f"https://users.roblox.com/v1/users/{UserID}"

def get_user_badges(user_id):
    all_badges = []
    cursor = ""
    while True:
        response = requests.get(f"{BadgesUrl}&cursor={cursor}").json()
        page = response.get("data", [])
        for badge in page:
            all_badges.append(str(badge["id"]))
        print(f"Badge IDs found on current page: {', '.join(id for id in all_badges[-len(page):])}")
        cursor = response.get("nextPageCursor")
        print(f"Currently on page: {cursor}")
        if not cursor:
            break
    return all_badges

def get_username(user_id):
    response = requests.get(UsersUrl).json()
    return response["name"]

all_badges = get_user_badges(UserID)

user_badges = get_user_badges(UserID)
username = get_username(UserID)
owned_badges = len(set(user_badges).intersection(Badge))

if owned_badges > 0:
    print(f"User owns {owned_badges} of the hunt badges")
else:
    print("User does not own any of the hunt badges")

webhook = DiscordWebhook(url=webhook_url, username="THE HUNT")

def send(webhook, embed):
    webhook.add_embed(embed)
    webhook.execute()

def main():
    embed = DiscordEmbed(title=":trophy: **𝗧𝗵𝗲 𝗛𝘂𝗻𝘁 𝗣𝗿𝗼𝗴𝗿𝗲𝘀𝘀** :trophy:", color=0x243dff)
    embed.add_embed_field(name="", value="")
    embed.add_embed_field(name=f":identification_card: **{username}**", value=f":gem:** `{owned_badges}` out of 100 badges **",inline=False)
    embed.add_embed_field(name="", value="")
    send(webhook, embed)
    print("Webhook sent successfully.")
  
if __name__ == "__main__":
    main()



