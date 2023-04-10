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

# Récupération des messages de la semaine dernière dans le canal #troll
start_of_week = (datetime.datetime.now() - datetime.timedelta(days=7)).timestamp()
try:
    response = client.conversations_history(channel="CTP15QXLZ", oldest=start_of_week)
    messages = response['messages']
except SlackApiError as e:
    print("Erreur lors de la récupération des messages : {}".format(e))

# Calcul du nombre total de réactions pour chaque message
reactions_count = {}
for msg in messages:
    count = 0
    for reaction in msg['reactions']:
        count += reaction['count']
    reactions_count[msg['ts']] = count

# Tri des messages par nombre total de réactions
top_messages = sorted(reactions_count.items(), key=lambda x: x[1], reverse=True)[:5]

# Construction du message à envoyer sur Slack
if top_messages:
    message = "Les 5 messages ayant reçu le plus de réactions la semaine dernière dans le canal #troll sont : \n\n"
    for i, msg in enumerate(top_messages):
        response = client.conversations_permalink(channel="CTP15QXLZ", message_ts=msg[0])
        permalink = response['permalink']
        text = response['message']['text']
        message += f"{i+1}. {text} ({msg[1]} réactions) : {permalink}\n"

    # Envoi du message sur Slack
    try:
        response = client.chat_postMessage(
            channel="CTP15QXLZ",
            text=message
        )
        print("Message envoyé : ", response['ts'])
    except SlackApiError as e:
        print("Erreur lors de l'envoi du message : {}".format(e))
else:
    print("Aucun message trouvé dans le canal #troll.")
