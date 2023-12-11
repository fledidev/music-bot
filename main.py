from flask import Flask
from dotenv import load_dotenv
import bot
import os

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"


if __name__ == '__main__':
    load_dotenv()
    bot.discord_bot.run_bot(os.getenv('DISCORD_API_KEY'))

    app.run(debug=True)