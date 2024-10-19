import telebot
from telebot import types

import admin
import db

db.create_table()

TOKEN = '8123736150:AAH5C8FIU7M1cS0cqJApzrfzq6_x0MU5ADI'

bot = telebot.TeleBot(TOKEN)


products = db.select_products()

basket = []

def main_menu():
    markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    item1 = types.KeyboardButton('Каталог')
    item2 = types.KeyboardButton('Корзина')
    markup.add(item1, item2)
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    if not db.auth_user(message.from_user.username):
        db.add_user(message.from_user.username,message.chat.id)
    bot.reply_to(message, 'Добро пожаловать в наш магазин!',reply_markup=main_menu())


@bot.message_handler(func=lambda message: message.text == 'Каталог')
def show_catalog(message):
    for product in products:
        img = open(product['img'], 'rb').read()
        bot.send_photo(message.chat.id, img, caption=f'Товар: {product['name']} Цена: {product['price']}', reply_markup=add_to_cart(product['id']))
        #bot.send_message(message.chat.id, f'Товар: {product['name']} Цена: {product['price']}', reply_markup=add_to_cart(product['id']))

def add_to_cart(product_id):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Добавить в корзину', callback_data=f'add_to_cart:{product_id}')
    markup.add(item1)
    return markup


@bot.callback_query_handler(func=lambda call: call.data.startswith('add_to_cart'))
def callback_inline(call):
    id = int(call.data.split(':')[1])
    basket.append(id)
    bot.answer_callback_query(call.id, 'Товар добавлен в корзину')
    bot.send_message(call.message.chat.id, 'Товар добавлен в корзину')


@bot.message_handler(func=lambda message: message.text == 'Корзина')
def show_basket(message):
    total = 0
    for b in basket:
        for product in products:
            if product['id'] == b:
                bot.send_message(message.chat.id, f'Id: {product['id']} Name: {product['name']} Price: {product['price']}')
                total += product['price']
    bot.send_message(message.chat.id, f'Общая сумма заказа {total} руб.')




@bot.message_handler(commands=['admin'])
def admin_admin(message):
    if db.admin(message.from_user.username):
        bot.send_message(message.chat.id, 'Добро пожаловать в админ-панель!', reply_markup=admin.admin_menu())
    else:
        bot.send_message(message.chat.id, 'У вас недостаточно прав!')


@bot.message_handler(func=lambda message: message.text == 'Добавить товар' and db.admin(message.from_user.username))
def add_product(message):
    admin.handle_add_product(bot, message)

@bot.message_handler(func=lambda message: message.text == 'Рассылка всем пользователям' and db.admin(message.from_user.username))
def ras_users(message):
    admin.handle_ras_users(bot, message)


@bot.message_handler(func=lambda message: message.text == 'Просмотр пользователей' and db.admin(message.from_user.username))
def view_users(message):
    users = db.select_users()
    for user in users:
        bot.send_message(message.chat.id,f'{user[0]}', reply_markup=delete_user(user[0]))



@bot.callback_query_handler(func=lambda call: call.data.startswith('delete_user'))
def del_userdb(call):
    nickname = call.data.split(':')[1]
    db.delete_user(nickname)
    bot.send_message(call.message.chat.id,  f'Пользователь с nickname {nickname} удален из базы данных')


def delete_user(user_id):
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton('Удалить', callback_data=f'delete_user:{user_id}')
    markup.add(item1)
    return markup


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    file_info = bot.get_file(message.photo[-1].file_id)
    downloaded_file = bot.download_file(file_info.file_path)
    src = 'files/photo_' + file_info.file_path.split('/')[-1]
    f = open(src, 'wb')
    f.write(downloaded_file)

    bot.reply_to(message, 'Фото сохранено!')



bot.polling()