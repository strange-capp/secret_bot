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


@app.route('/{}'.format(bot_token),
           methods=['POST'])
def index():
    response = request.get_json(force=True)
    bot = SecretBot(token=bot_token, data=response, name='secret_bot')

    print(str(response))

    is_sent = bot.send_secret()

    if is_sent:
        return "200"
    else:
        return 'ex'

@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=heroku_url, HOOK=bot_token))
    if s:
        return "webhook setup ok"
    else:
        return "webhook setup failed"