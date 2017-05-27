import keys
from iso import iso
import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


def greet_user(bot, update):
    print('Called /start')
    lst_terms = []
    for d_key in iso:
        lst_terms.append(d_key)
    all_terms = ', \n'.join(lst_terms)
    update.message.reply_text(all_terms)


def talk_to_me(bot, update):
    user_text = update.message.text.lower()
    print(user_text)
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


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log'
                    )


def main():
    updater = Updater(keys.API_KEY)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', greet_user))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))

    updater.start_polling()
    updater.idle()

main()
