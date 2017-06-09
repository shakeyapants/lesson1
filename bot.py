import keys
import ephem
import time
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup
from nums import nums


# dictionary for separate calculation for each user
user_texts = {}


# First and last name of the user
def get_user_name(update):
    user_name = update.message.chat.first_name + ' ' + update.message.chat.last_name
    return user_name


def greet_user(bot, update):
    user_name = get_user_name(update)
    print('{} called /start'.format(user_name))
    update.message.reply_text('Привет, {}'.format(user_name))


def calculation(bot, update):
    chat_id = update.message.chat_id
    logging.info('{} called /start'.format(get_user_name(update)))

    custom_keyboard = [['7', '8', '9', '+'],
                       ['4', '5', '6', '-'],
                       ['1', '2', '3', '*'],
                       ['0', '/', '=']]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)

    bot.send_message(chat_id=chat_id,
                     text="Please enter calculation",
                     reply_markup=reply_markup)


def planet_today(bot, update):
    user_name = get_user_name(update)
    user_text = update.message.text
    print('{} wrote {}'.format(user_name, user_text))
    planet = user_text.split()[1]
    today = time.strftime('%Y/%m/%d')
    if planet == 'Mercury':
        today_in = ephem.constellation(ephem.Mercury(today))
    elif planet == 'Venus':
        today_in = ephem.constellation(ephem.Venus(today))
    elif planet == 'Earth':
        update.message.reply_text('No-no-no, try something different')
    elif planet == 'Mars':
        today_in = ephem.constellation(ephem.Mars(today))
    elif planet == 'Jupiter':
        today_in = ephem.constellation(ephem.Jupiter(today))
    elif planet == 'Saturn':
        today_in = ephem.constellation(ephem.Saturn(today))
    elif planet == 'Uranus':
        today_in = ephem.constellation(ephem.Uranus(today))
    elif planet == 'Neptune':
        today_in = ephem.constellation(ephem.Neptune(today))
    elif planet == 'Pluto':
        today_in = ephem.constellation(ephem.Pluto(today))
    else:
        update.message.reply_text('There\'s no such planet (respect planets and write them with capital letter!)')

    answer = today_in[1]
    update.message.reply_text('Today {} is in {}'.format(planet, answer))


def talk_to_me(bot, update):
    user_name = get_user_name(update)
    user_text = update.message.text.lower()
    print(user_text)
    list_user_text = user_texts.setdefault(update.message.chat_id, [])
    list_user_text.append(user_text)
    print('{} wrote {}'.format(user_name, user_text))

    if list_user_text[-1] == '=':
        user_text = ''.join(list_user_text)
        del list_user_text[:]

    if user_text.startswith('сколько будет'):
        user_calc = user_text[13:]
        user_calc_clear = user_calc.replace('?', '')
        list_user_words = user_calc_clear.split()

        for word in list_user_words:
            if word not in nums:
                list_user_words.remove(word)

        for i in range(len(list_user_words)):
            list_user_words[i] = nums.get(list_user_words[i])

        user_text = ''.join(list_user_words) + '='

        user_texts.pop(update.message.chat_id)
    if user_text.endswith('='):
        try:
            if '-' in user_text:
                num1 = int(user_text.split('-')[0])
                part2 = user_text.split('-')[1]
                num2 = int(part2.strip('='))
                reply = num1 - num2
            elif '+' in user_text:
                num1 = int(user_text.split('+')[0])
                part2 = user_text.split('+')[1]
                num2 = int(part2.strip('='))
                reply = num1 + num2
            elif '/' in user_text:
                num1 = int(user_text.split('/')[0])
                part2 = user_text.split('/')[1]
                num2 = int(part2.strip('='))
                try:
                    reply = num1 / num2
                except ZeroDivisionError:
                    reply = 'Division by zero hurts!'
            elif '*' in user_text:
                num1 = int(user_text.split('*')[0])
                part2 = user_text.split('*')[1]
                num2 = int(part2.strip('='))
                reply = num1 * num2
        except ValueError:
            reply = 'Seems like no numbers to calculate'
    update.message.reply_text(reply)


def wordcount(bot, update):
    user_text = update.message.text
    text = user_text[10:]
    clear_text = text.strip()
    if clear_text.startswith('"') and clear_text.endswith('"'):
        words = clear_text.split()
        update.message.reply_text(len(words))

    else:
        update.message.reply_text('The string must be in quotes')


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    updater = Updater(keys.API_KEY)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('calc', calculation))
    dp.add_handler(CommandHandler('planet', planet_today))
    dp.add_handler(CommandHandler('wordcount', wordcount))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    logging.info('Bot started')
    main()
