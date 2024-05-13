import os
import io
import fitz
import telebot
from PIL import Image

# Замените токен на свой токен бота
TOKEN = '6937186827:AAHzl9HI5S4cnPv_ckk47fXSDbEgGMD9Pl4'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(content_types=['document'])
def handle_document(message):
    file_info = bot.get_file(message.document.file_id)
    downloaded_file = bot.download_file(file_info.file_path)

    src = 'temp.pdf'
    with open(src, 'wb') as new_file:
        new_file.write(downloaded_file)

    doc = fitz.open(src)
    page = doc[0]
    pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))  # увеличиваем масштаб в 2 раза

    output_filename = 'output.png'
    pix.save(output_filename)

    doc.close()  # закрываем файл перед удалением

    with open(output_filename, 'rb') as photo:
        bot.send_photo(message.chat.id, photo)

    os.remove(src)
    os.remove(output_filename)

bot.polling()
