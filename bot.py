import telebot
from flask import Flask, request
import os

TOKEN = "8726956835:AAGLYnQnVf5ge3yAcsZFXEXu7wrof..."
MY_ID = 8710784205

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__) # ប្ដូរមកប្រើពាក្យ app វិញ

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot ដំណើរការជោគជ័យហើយ!")

@bot.message_handler(func=lambda message: True)
def forward_msg(message):
    info = f"👤 User: {message.from_user.first_name}"
    if message.content_type == 'text':
        bot.send_message(MY_ID, f"{info}\n💬 Message: {message.text}")

@app.route('/' + TOKEN, methods=['POST']) # ប្ដូរមកប្រើ app
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route("/") # ប្ដូរមកប្រើ app
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url="https://my-forwarding-bot.onrender.com/" + TOKEN)
    return "Webhook set successfully!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000))) # ប្ដូរមកប្រើ app
