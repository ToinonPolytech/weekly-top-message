import os
from slack_bolt import App
from datetime import datetime, timedelta

app = App(token=os.environ["SLACK_BOT_TOKEN"])

# Fonction pour trier les messages par nombre de réactions
def sort_by_reaction_count(messages):
    sorted_messages = sorted(messages, key=lambda x: len(x['reactions']), reverse=True)
    return sorted_messages[:5]

# Fonction pour récupérer les messages de la semaine dernière
def get_last_week_messages(channel_id):
    last_week = (datetime.today() - timedelta(days=7)).strftime('%s')
    try:
        response = app.client.conversations_history(
            channel=channel_id,
            oldest=last_week
        )
        return response['messages']
    except SlackApiError as e:
        print("Error retrieving messages: {}".format(e))

# Fonction pour créer le classement des messages sous forme de blocs Slack
def create_leaderboard_blocks(messages):
    leaderboard_blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": "*Classement des 5 messages les plus populaires de la semaine dernière :*"
            }
        }
    ]
    for i, m in enumerate(messages):
        leaderboard_blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": f"{i+1}. <{m['permalink']}|{m['text']}> - {len(m['reactions'])} réactions"
                }
            }
        )
    return leaderboard_blocks

# Envoi du message de classement chaque lundi à 9h
@app.schedule("cron", hour="9", day_of_week="1")
def send_leaderboard_message():
    # Récupérer les messages du canal
    messages = get_last_week_messages(channel_id='#general')
    # Trier les messages par nombre de réactions
    sorted_messages = sort_by_reaction_count(messages)
    # Créer les blocs de classement
    leaderboard_blocks = create_leaderboard_blocks(sorted_messages)
    # Envoyer le message dans le canal
    response = app.client.chat_postMessage(
        channel='#troll',
        blocks=leaderboard_blocks
    )
    print(response)

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
