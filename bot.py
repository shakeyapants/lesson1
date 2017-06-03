import keys
import ephem
import time
from iso import iso
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def get_user_name(update):
    user_name = update.message.chat.first_name + ' ' + update.message.chat.last_name
    return user_name


def greet_user(bot, update):
    user_name = get_user_name(update)
    print('{} called /start'.format(user_name))
    logging.info('{} called /start'.format(user_name))
    lst_terms = []
    for d_key in iso:
        lst_terms.append(d_key)
    all_terms = ', \n'.join(lst_terms)
    update.message.reply_text(all_terms)


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
    print('{} wrote {}'.format(user_name, user_text))
    possible_keys = []
    for d_key in iso:
        if user_text in d_key:
            possible_keys.append(d_key)

    if len(possible_keys) == 0:
        reply = 'Такого определения нет, может опечатка?'
    elif len(possible_keys) == 1:
        reply = possible_keys[0] + ' – это ' + iso.get(possible_keys[0])
    else:
        possible_replies = ', '.join(possible_keys)
        reply = 'Есть несколько определений, уточни запрос: ' + possible_replies
    update.message.reply_text(reply)


logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    updater = Updater(keys.API_KEY)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(CommandHandler('planet', planet_today))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    logging.info('Bot started')
    main()
