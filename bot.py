import telebot
from flask import Flask, request
import os

# ដាក់ TOKEN និង ID របស់អ្នកឱ្យត្រឹមត្រូវ
TOKEN = "8726956835:AAGLYnQnVf5ge3yAcsZFXEXu7wrof..."
MY_ID = 8710784205

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Bot កំពុងដំណើរការលើ Render រួចរាល់ហើយ!")

@bot.message_handler(func=lambda message: True)
def forward_msg(message):
    info = f"👤 User: {message.from_user.first_name}\n🆔 ID: {message.from_user.id}"
    if message.content_type == 'text':
        bot.send_message(MY_ID, f"{info}\n💬 Message: {message.text}")
    elif message.content_type == 'photo':
        bot.send_photo(MY_ID, message.photo[-1].file_id, caption=info)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    return "Bot is running!", 200

if __name__ == "__main__":
    # នេះជាផ្នែកសំខាន់ដើម្បីឱ្យ Render ដើរ (Port)
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
