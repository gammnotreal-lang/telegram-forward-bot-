import telebot
from flask import Flask, request
import os

TOKEN = "8726956835:AAGLYnQnVf5ge3yAcsZFXEXu7wrofrqQ_Os"
MY_ID = 8710784205

bot = telebot.TeleBot(TOKEN)
server = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "សួស្ដី! Bot កំពុងដំណើរការលើ Render។")

@bot.message_handler(func=lambda message: message.chat.id != MY_ID, content_types=['text', 'photo', 'sticker'])
def forward_msg(message):
    username = f"@{message.from_user.username}" if message.from_user.username else "គ្មាន"
    info = f"👤 User: {message.from_user.first_name}\n📛 Username: {username}\n🆔 ID: {message.from_user.id}"
    
    if message.content_type == 'text':
        bot.send_message(MY_ID, f"{info}\n💬 Message: {message.text}")
    elif message.content_type == 'photo':
        bot.send_photo(MY_ID, message.photo[-1].file_id, caption=f"{info}\n🖼 (រូបភាព)")
    elif message.content_type == 'sticker':
        bot.send_message(MY_ID, f"{info}\n✨ (Sticker)")
        bot.send_sticker(MY_ID, message.sticker.file_id)

@server.route('/' + TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@server.route("/")
def webhook():
    bot.remove_webhook()
    # ចំណាំ៖ Link ខាងក្រោមនេះអ្នកត្រូវប្ដូរក្រោយពេលបង្កើត Web Service ក្នុង Render រួច
    # bot.set_webhook(url="https://ឈ្មោះ-app-របស់អ្នក.onrender.com/" + TOKEN)
    return "Bot is Running!", 200

if __name__ == "__main__":
    server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
