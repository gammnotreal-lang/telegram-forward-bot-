import telebot
from flask import Flask, request
import os

TOKEN = "8726956835:AAGLYnQnVf5ge3yAcsZFXEXu7wrofrqQ_Os"
MY_ID = 8710784205

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ផ្លូវដើមសម្រាប់ឆែកមើលថា Server ដើរឬអត់
@app.route('/')
def index():
    return "Bot is Live!", 200

# ផ្លូវសម្រាប់ទទួលសារពី Telegram
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

# ផ្លូវសម្រាប់ដំឡើង Webhook (ចុច Link នេះដើម្បីឱ្យ Bot ដើរ)
@app.route("/set_webhook")
def webhook_setup():
    bot.remove_webhook()
    url = f"https://my-forwarding-bot.onrender.com/{TOKEN}"
    status = bot.set_webhook(url=url)
    if status:
        return "Webhook set successfully!", 200
    return "Webhook failed!", 400

# មុខងារ Forward សារ
@bot.message_handler(func=lambda message: True)
def forward_msg(message):
    try:
        sender = message.from_user.first_name
        bot.send_message(MY_ID, f"👤 ពី: {sender}\n💬 សារ: {message.text}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
