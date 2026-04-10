import telebot
from flask import Flask, request
import os

# Token ថ្មីដែលអ្នកបានផ្ដល់ឱ្យ
TOKEN = "8726956835:AAGLYnQnVf5ge3yAcsZFXEXu7wrofrqQ_Os"
MY_ID = 8710784205

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/")
def webhook():
    bot.remove_webhook()
    # ប្រើ Link Render របស់អ្នក
    status = bot.set_webhook(url="https://my-forwarding-bot.onrender.com/" + TOKEN)
    if status:
        return "Webhook set successfully!", 200
    else:
        return "Webhook failed!", 400

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot ដំណើរការជោគជ័យហើយ! ខ្ញុំនឹង Forward សារជូនអ្នក។")

@bot.message_handler(func=lambda message: True)
def forward_msg(message):
    info = f"👤 ពី: {message.from_user.first_name}"
    if message.content_type == 'text':
        bot.send_message(MY_ID, f"{info}\n💬 សារ: {message.text}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
