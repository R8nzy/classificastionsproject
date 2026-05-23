import telebot
import os
from classification import detect


bot = telebot.TeleBot("8114129500:AAHvASiTbEPAGxlP-mNeZEVM8u1tQ-MiVs4")
@bot.message_handler(commands=['start',"play"])
def send_welcome(message):
    bot.reply_to(message, "Привет! Я твой Telegram бот. Напиши что-нибудь!")


@bot.message_handler(content_types=["photo"])
def take_photo(message):
    if not message.photo:
        return
    info = bot.get_file(message.photo[-1].file_id)
    name = info.file_path.split("/")[-1]
    save_tg = bot.download_file(info.file_path)
    with open(name, "wb") as f:
        f.write(save_tg)    
    class_name, proc = detect(f"./{name}", "./models/model1.h5", "./models/labels.txt")
    class_name = class_name.replace("\n", "").lower()
    proc = int(proc * 100 // 1)
    bot.reply_to(message, f"На изображении {class_name} с вероятностью {proc}%")
    os.remove(f"./{name}")


bot.infinity_polling()
