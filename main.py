from flask import Flask, render_template
from dotenv import load_dotenv
import bot
import source
import os

app = Flask(__name__)
app.template_folder = 'web/templates'
app.static_folder = 'web/static'


@app.route("/")
def home():
    return render_template("index.html")


if __name__ == '__main__':
    # load_dotenv()
    # source.manager.download_video("https://www.youtube.com/watch?v=XXYlFuWEuKI")
    # bot.discord_bot.run_bot(os.getenv('DISCORD_API_KEY'))
    app.run(debug=True)
