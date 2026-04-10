import telebot
from flask import Flask, request
import os

# ប្រើ Token និង ID ដែលអ្នកបានផ្ដល់ឱ្យ
TOKEN = "8726956835:AAGLYnQnVf5ge3yAcsZFXEXu7wrofrqQ_Os"
MY_ID = 8710784205

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Route សម្រាប់ឆែកមើលថា Server ដើរឬអត់ និងការពារ Error [HEAD]
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return "Bot is running!", 200

# Route សម្រាប់ទទួលសារពី Telegram
@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    if request.headers.get('content-type') == 'application/json':
        json_string = request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return "!", 200
    return "Invalid", 403

# Route សម្រាប់ដំឡើង Webhook (ជំហានបង្កឱ្យ Bot ភ្ញាក់)
@app.route("/set_webhook")
def webhook_setup():
    bot.remove_webhook()
    url = f"https://my-forwarding-bot.onrender.com/{TOKEN}"
    status = bot.set_webhook(url=url)
    if status:
        return "<h1>Webhook set successfully!</h1>", 200
    return "<h1>Webhook failed!</h1>", 400

# មុខងារ Forward សារ
@bot.message_handler(func=lambda message: True)
def forward_msg(message):
    try:
        info = f"👤 ពី: {message.from_user.first_name}"
        bot.send_message(MY_ID, f"{info}\n💬 សារ: {message.text}")
    except Exception as e:
        print(f"Error forwarding: {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
