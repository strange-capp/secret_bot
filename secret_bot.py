from flask import Flask, request, render_template
from bot.bots import SecretBot
import telegram
import os

app = Flask(__name__)


def get_token():
    token = os.environ.get('BOT_TOKEN')

    return token


bot_token = get_token()

# credentials to set up webhooks
bot = telegram.Bot(token=bot_token)
heroku_url = 'https://secret-bott.herokuapp.com/'


# views
@app.route('/')
def rocket():
    return render_template('spaceship.html')


@app.route('/{}'.format(bot_token),
           methods=['POST'])
def index():
    response = request.get_json(force=True)
    secret_bot = SecretBot(token=bot_token, data=response, name='secret_bot')
    if secret_bot.text == '/get':
        secret_bot.send_secret()
    else:
        secret_bot.send_text('Просто попроси... (/get)')

    if secret_bot.name_of_interlocutor == 'ttt':
        print(secret_bot.current_chat_id)

    secret_bot.send_text('New message to ' + str(secret_bot.username_of_interlocutor),
                         chat_id=782633810)

    return 'ex'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=heroku_url, HOOK=bot_token))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
