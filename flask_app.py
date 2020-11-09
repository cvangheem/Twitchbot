from flask import Flask, render_template, app
from jinja2 import Environment, FileSystemLoader, select_autoescape

app = Flask(__name__)
env = Environment(
    loader=FileSystemLoader('C:/Users/cvang/Documents/Twitch Stream/Working '
                            'Code/PythonTwitchBotFramework-master/templates'),
    autoescape=select_autoescape(['html', 'xml'])
)
template = env.get_template('bot_overlay.html')

@app.route("/",methods=["POST","GET","DELETE"])
def print_answer(*answer):
    with app.app_context():
        return render_template('bot_overlay.html', answer=answer)
# you can add aditional routes or functions as required
