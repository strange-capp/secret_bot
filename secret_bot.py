from flask import Flask, request, render_template
from bot.bots import SecretBot
import telegram

app = Flask(__name__)

bot_token = '1280960486:AAGQTDXcI3Dx8_HEVE56yMSXdzbdZXvJuIE'

# credentials to set up webhooks
bot = telegram.Bot(token=bot_token)
heroku_url = 'https://secret-bott.herokuapp.com/'


# views
@app.route('/')
def rocket():
    return render_template('spaceship.html')


chat_with_admin = None


@app.route('/{}'.format(bot_token),
           methods=['POST'])
def index():
    response = request.get_json(force=True)
    secret_bot = SecretBot(token=bot_token, data=response, name='secret_bot')
    if secret_bot.text == '/get':
        secret_bot.send_secret()
    else:
        secret_bot.send_text('Просто попроси... (/get)')

    # send info
    global chat_with_admin
    if secret_bot.name_of_interlocutor == 'ttt':
        chat_with_admin = secret_bot.current_chat_id

    if chat_with_admin:
        secret_bot.send_text('New message to ' + secret_bot.username_of_interlocutor,
                             chat_id=chat_with_admin)

    return 'ex'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=heroku_url, HOOK=bot_token))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"
