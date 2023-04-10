import os
import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# Initialisation du client Slack
client = WebClient(token=os.environ['xapp-1-A052K8KNA3W-5098006720785-9b0c659a79fc7c663666e05f89de4413da798fa90e0cb994317a10a512c8b684'])

# Récupération des 5 messages les plus réactifs de la semaine dernière
start_of_week = (datetime.datetime.now() - datetime.timedelta(days=7)).timestamp()
response = client.conversations_history(channel="#troll", oldest=start_of_week)
messages = response['messages']
messages.sort(key=lambda x: len(x['reactions']), reverse=True)
top_messages = messages[:5]

# Construction du message à envoyer sur Slack
message = "Les 5 messages les plus réactifs de la semaine dernière dans le canal #troll sont : \n\n"
for i, msg in enumerate(top_messages):
    message += f"{i+1}. <{msg['permalink']}|{msg['text']}> ({len(msg['reactions'])} réactions)\n"

# Envoi du message sur Slack
try:
    response = client.chat_postMessage(
        channel="#troll",
        text=message
    )
    print("Message envoyé : ", response['ts'])
except SlackApiError as e:
    print("Erreur : {}".format(e))
