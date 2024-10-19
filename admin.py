from telebot import types

import db


def admin_menu():
    row = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    item1 = types.KeyboardButton('Добавить товар')
    item2 = types.KeyboardButton('Просмотр пользователей')
    item3 = types.KeyboardButton('Рассылка всем пользователям')
    row.add(item1, item2, item3)
    return row


def handle_add_product(bot, message):
    msg = bot.reply_to(message, 'Введите название')
    bot.register_next_step_handler(msg, lambda m: handle_product_name(bot, m))

def handle_product_name(bot, message):
    product_name = message.text
    msg = bot.reply_to(message, f'Название товара {product_name} Введите цену товара: ')
    bot.register_next_step_handler(msg, lambda m: handle_product_price(bot, m, product_name))

def handle_product_price(bot, message, product_name):
    price = int(message.text)
    db.add_product(product_name, price)
    bot.reply_to(message, f'Товар {product_name} с ценой {price} добавлен')

def handle_ras_users(bot, message):
    msg = bot.reply_to(message, 'Загрузите изображеие')
    bot.register_next_step_handler(msg, lambda m: handle_ras_users_new(bot, m))
    #file_info = bot.get_file(message.photo[-1].file_id)
    #file_info = bot.get_file(message.photo[-1].file_id)
    #downloaded_file = bot.download_file(file_info.file_path)
    #print(downloaded_file)

def handle_ras_users_new(bot, message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    users = db.select_users()
    for user in users:
        bot.send_photo(user[1], downloaded_file, caption=message.text)
