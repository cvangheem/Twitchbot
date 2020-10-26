from twitchbot import BaseBot, PubSubData, PubSubSubscription
import flask_app as fa

if __name__ == '__main__':
    BaseBot().run()
    fa.app.run(debug=True)