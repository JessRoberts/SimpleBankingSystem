# Write your code here
import random
import sqlite3
conn = sqlite3.connect('card.s3db')
cur = conn.cursor()
#cur.execute('DROP TABLE card')
#conn.commit()
cur.execute('CREATE TABLE IF NOT EXISTS card (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0);')
conn.commit()

class Banking:
    balance = 0
    card_number = ()
    pin_number = ()
    trans_card = ()
    trans_amount = ()

    def __init__(self):
        menu()

def menu():
    print("1. Create an account")
    print("2. Log into account")
    print("0. Exit")
    x = int(input())
    if x == 1:
        create()
    elif x == 2:
        login()
    else:
        print('Bye!')
        exit()

def luhn_check ():
    luhn_check_1 = [int(i) for i in str(Banking.trans_card[:15])]
    luhn_checksum = Banking.trans_card[-1]
    k = 2
    luhn_check_1[0::2] = [x * k for x in luhn_check_1[0::2]]
    luhn_check_1 = [x -9 if x > 9 else x for x in luhn_check_1]
    luhn_addition = sum(luhn_check_1)
    if (int(luhn_addition) + int(luhn_checksum)) % 10 != 0:
        print('Probably you made mistake in the card number. Please try again!')
        account()

def luhn_test():
    results = int(f"{random.randint(400000000000000, 400000999999999):15}")
    Banking.pin_number = f"{random.randint(0000, 9999):04}"
    checksum = 0
    luhn = results + checksum
    pro_check = [int(i) for i in str(luhn)]
    k = 2
    pro_check[0::2] = [x * k for x in pro_check[0::2]]
    pro_check = [x -9 if x > 9 else x for x in pro_check]
    addition = sum(pro_check)
    while (addition + checksum) % 10 != 0:
        checksum += 1
    results = f"{results}{checksum}"
    Banking.card_number = str(results)
    Banking.pin_number = str(Banking.pin_number)
    cid = str(Banking.card_number)[6:16]
    cur.execute(f'INSERT INTO card (id, number, pin) VALUES ({cid}, {Banking.card_number}, {Banking.pin_number})')
    conn.commit()
    return

def create():
    print("Your card has been created")
    print("Your card number:")
    luhn_test()
    print(Banking.card_number)
    print("Your card PIN:")
    print(Banking.pin_number)

def login():
    print("Enter your card number:")
    logincard = int(input())
    Banking.card_number = logincard
    print("Enter your PIN:")
    loginpin = int(input())
    Banking.pin_number = loginpin
    cur.execute(f'SELECT * FROM card WHERE number = "%s" and pin = "%s"' % (logincard, loginpin))
    if cur.fetchone() is not None:
        print("You have successfully logged in!")
        account()
    else:
        print("Wrong card number or PIN!")
        menu()


def account():
    print("1. Balance")
    print("2. Add income")
    print("3. Do transfer")
    print("4. Close account")
    print("5. Log out")
    print("0. Exit")
    y = int(input())
    if y == 1:
        cur.execute(f'SELECT balance FROM card WHERE number = {Banking.card_number}')
        conn.commit()
        balance_print = cur.fetchone()
        print('Balance:', balance_print)
        account()
    elif y == 2:
        print('Enter income:')
        money = input()
        cur.execute(f'UPDATE card SET balance = balance + {money} WHERE number = {Banking.card_number}')
        conn.commit()
        print('Income was added')
        account()
    elif y == 3:
        print('Transfer')
        print('Enter card number:')
        trans_card = input()
        Banking.trans_card = trans_card
        luhn_check()
        cur.execute(f'SELECT * FROM card WHERE number = "%s"' % (Banking.trans_card))
        conn.commit()
        d = cur.fetchone()
        if d == Banking.card_number:
            print('Probably you made mistake in the card number. Please try again!')
        if d is None:
            print('Such a card does not exist.')
            account()
        elif d is not None:
            print('Enter how much money you want to transfer:')
            trans_amount = input()
            Banking.trans_amount = trans_amount
            cur.execute(f'SELECT balance FROM card WHERE number = {Banking.card_number}')
            conn.commit()
            if int(cur.fetchone()[0]) < int(trans_amount):
                print('Not enough money!')
                account()
            else:
                cur.execute(f'UPDATE card SET balance = balance + {Banking.trans_amount} WHERE number = {Banking.trans_card}')
                conn.commit()
                cur.execute(f'UPDATE card SET balance = balance - {Banking.trans_amount} WHERE number = {Banking.card_number}')
                conn.commit()
                print('Success!')
                menu()

    elif y == 4:
        cur.execute(f'DELETE FROM card WHERE number = {Banking.card_number};')
        conn.commit()
        print('The account has been closed!')
        account()
    elif y == 5:
        Banking.card_number = 0
        Banking.pin_number = 0
        print("You have successfully logged out!")
    else:
        print("Bye!")
        exit()

while True:
    Banking()
