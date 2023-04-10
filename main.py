import os
import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Chargement des variables d'environnement depuis le fichier .env
load_dotenv()

# Récupération du token d'API Slack depuis la variable d'environnement
slack_api_token = os.getenv('SLACK_BOT_TOKEN')

# Initialisation du client Slack
client = WebClient(token=slack_api_token)

# Récupération des 5 messages les plus réactifs de la semaine dernière
start_of_week = (datetime.datetime.now() - datetime.timedelta(days=7)).timestamp()
try:
    response = client.conversations_history(channel="#troll", oldest=start_of_week)
    print(response['messages'])
    messages = response['messages']
    messages.sort(key=lambda x: len(x['reactions']), reverse=True)
    top_messages = messages[:5]
    print("Les messages ont été récupérés avec succès.")
except SlackApiError as e:
    print("Erreur lors de la récupération des messages : {}".format(e))

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
    print("Erreur lors de l'envoi du message : {}".format(e))
