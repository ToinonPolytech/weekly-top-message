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

# Récupération des messages les plus réactifs de la semaine dernière
start_of_week = (datetime.datetime.now() - datetime.timedelta(days=7)).timestamp()
try:
    response = client.conversations_history(channel="CTP15QXLZ", oldest=start_of_week)
    messages = response['messages']
    messages.sort(key=lambda x: len(x.get('reactions', [])), reverse=True)
    top_messages = messages[:5]
except SlackApiError as e:
    print("Erreur lors de la récupération des messages : {}".format(e))

# Construction du message à envoyer sur Slack
if top_messages:
    message = "Les 5 messages les plus réactifs de la semaine dernière dans le canal #troll sont : \n\n"
    for i, msg in enumerate(top_messages):
        text = msg.get('text')[:40] + '...' if len(msg.get('text')) > 40 else msg.get('text')
        permalink = msg.get('permalink_public')
        count_reactions = sum([r['count'] for r in msg.get('reactions', [])])
        message += f"{i+1}. {text} ({count_reactions} réactions) : {permalink}\n"

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
