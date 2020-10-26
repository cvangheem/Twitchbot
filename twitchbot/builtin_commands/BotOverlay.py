from flask import Flask, render_template

app=Flask(__name__)
@app.route("/",methods=["POST","GET","DELETE"])
def home():
    x="a variable"
    return render_template('bot_overlay.html', answer=x)

if __name__ == '__main__':
    app.run(debug=True)
