import telebot
from flask import Flask, request
import os

# ព័ត៌មានដែលអ្នកបានផ្ដល់ឱ្យ
TOKEN = "8726956835:AAGLYnQnVf5ge3yAcsZFXEXu7wrofrqQ_Os"
MY_ID = 8710784205

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# សម្រាប់ឆែកមើលថា Server ដើរឬអត់
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return "Bot is running!", 200

# ផ្លូវសម្រាប់ទទួលសារពី Telegram
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    return "Invalid", 403

# ផ្លូវសម្រាប់ដំឡើង Webhook (សំខាន់បំផុត)
@app.route("/set_webhook")
def webhook_setup():
    bot.remove_webhook()
    # ប្រើ Link របស់អ្នកឱ្យត្រូវតាម Render
    url = f"https://my-forwarding-bot.onrender.com/{TOKEN}"
    status = bot.set_webhook(url=url)
    if status:
        return "<h1>Webhook set successfully!</h1><p>Bot របស់អ្នកចាប់ផ្ដើមដំណើរការហើយ។</p>", 200
    return "<h1>Webhook failed!</h1>", 400

# មុខងារ Forward សារ
@bot.message_handler(func=lambda message: True)
def forward_msg(message):
    try:
        # បង្ហាញឈ្មោះអ្នកផ្ញើ និងសារ
        sender_name = message.from_user.first_name
        text_received = message.text
        bot.send_message(MY_ID, f"👤 ពី: {sender_name}\n💬 សារ: {text_received}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
