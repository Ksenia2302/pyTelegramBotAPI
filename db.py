import sqlite3

def connect():
    con = sqlite3.connect('shop.db')
    return con


def create_table():
    con = connect()
    cursor = con.cursor()
    cursor.execute('create table if not exists users (nickname text, chat_id integer, admin integer default 0)')
    con.commit()
    cursor.execute('create table if not exists products (id integer auto_increment, name text, price integer, photo text)')
    con.commit()


def add_user(nickname, chat_id):
    con = connect()
    cursor = con.cursor()
    cursor.execute('insert into users (nickname,chat_id) values (?,?)',(nickname, chat_id))
    con.commit()

def auth_user(nickname):
    con = connect()
    cursor = con.cursor()
    cursor.execute('select * from users where nickname = ?', (nickname,))
    if cursor.fetchone():
        return True
    return False

def select_products():
    con = connect()
    cursor = con.cursor()
    cursor.execute('select * from products')
    products = []
    for i in cursor.fetchall():
        products.append({
            'id': i[0],
            'name': i[1],
            'price': i[2],
            'img': i[3]
        })
    return products


def admin(nickname):
    con = connect()
    cursor = con.cursor()
    cursor.execute('select * from users where nickname = ?', (nickname,))
    admin_p = cursor.fetchone()[-1]
    if admin_p == 1:
        return True
    return False


def add_product(product_name, price):
    con = connect()
    cursor = con.cursor()
    cursor.execute('insert into products (name, price) values (?,?)', (product_name, price))
    con.commit()



def select_users():
    con = connect()
    cursor = con.cursor()
    cursor.execute('select * from users')

    return cursor.fetchall()

def delete_user(nickname):
    con = connect()
    cursor = con.cursor()
    cursor.execute('delete from users where nickname = ?', (nickname,))
    con.commit()
