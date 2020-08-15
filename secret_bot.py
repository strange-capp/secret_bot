from flask import Flask, request, render_template
from bot.bots import SecretBot

app = Flask(__name__)

bot_token = '1280960486:AAGQTDXcI3Dx8_HEVE56yMSXdzbdZXvJuIE'


@app.route('/')
def rocket():
    return render_template('spaceship.html')


@app.route('/1280960486:AAGQTDXcI3Dx8_HEVE56yMSXdzbdZXvJuIE1280960486:AAGQTDXcI3Dx8_HEVE56yMSXdzbdZXvJuIE',
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
