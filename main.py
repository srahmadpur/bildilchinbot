from json import JSONDecodeError

import telebot
import requests
import html2text
import logging
import time


logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

#logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                   # level=logging.DEBUG)
#logger = logging.getLogger(__name__)
#logging.warning("Start logging")


knownUsers = []  # save these in a file,
userStep = {}  # so they won't reset every time the bot restarts


def get_user_step(uid):
    if uid in userStep:
        return userStep[uid]
    else:
        knownUsers.append(uid)
        userStep[uid] = 0
        print("New user detected, who hasn't used \"/start\" yet")
        return 0


# only used for console output now
def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text' or "pinned_message":
            # print the sent message to the console
            t = time.localtime()
            current_time = time.strftime("%d %b %Y %H:%M:%S", t)
            print(str(current_time) + " " + str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + str(m.text))
            # f = open("UH-log.txt", 'a')
            # f.write(
            #   str(current_time) + " " + str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + str(m.text) + "\r")
            # f.close()


bot = telebot.TeleBot("1067624262:AAH2OCc7iyXYufX0WuEVQdhHeW5NsURLaTI")
bot.set_update_listener(listener)  # register listener


# @bot.message_handler(commands=["start"])
# def lang_chs(m):
#    cid = m.chat.id
#    bot.send_message(cid, "Hello there, lets choose language!")
#    markup = types.ReplyKeyboardMarkup()
#    item1 = types.KeyboardButton('AZ')
#    item2 = types.KeyboardButton('RU')
#    item3 = types.KeyboardButton('EN')
#    markup.row(item1, item2, item3)
#    bot.send_message(cid, "Choose one language:", reply_markup=markup)
#    bot.send_message(types.ReplyKeyboardRemove(selective=False))


@bot.message_handler(commands=["start"])
def send_echo(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, "Bildilçinə xoş gəldin!")
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, "Zəhmət olmasa axtarış dilini seç: /AZ , /RU , /EN")
    # time.sleep(5)


@bot.message_handler(commands=["AZ"])
def src_az(m):
    cid = m.chat.id
    sent = bot.send_message(cid, "Axtarmaq istədiyiniz sözü daxil edin:")
    bot.register_next_step_handler(sent, get_info_az)
    # INFO GET


def get_info_az(m):
    cid = m.chat.id
    print()
    src = m.text
    # print(src)
    r = requests.get('https://bildilchin.az:8888/bildilchin/get/description?selectedWord=' + str(src) + '&indexLang=az')
    r = r.json()
    if len(r) > 0:
        for word in r:
            a = word["description"]
            a = html2text.html2text(a)
            # print(a)
            bot.send_chat_action(cid, 'typing')
            bot.send_message(cid, str(src) + "  -sözünə əsasən axtarış nəticələri: ")
            if len(a) > 4096:
                for x in range(0, len(a), 4096):
                    bot.send_message(cid, a[x:x + 4096])
            else:
                bot.send_message(cid, a)
            bot.send_message(cid, "Yeni söz axtarmaq üçün /start və ya /AZ  komandasından istifadə et!")
            break
    else:
        bot.send_message(cid,
                         "Axtardığınız söz tapılmadı!  Yeni söz axtarmaq üçün /start və ya /AZ komandasından istifadə "
                         "et!")


@bot.message_handler(commands=["RU"])
def src_ru(m):
    cid = m.chat.id
    sent = bot.send_message(cid, "Введите слово, которое вы хотите найти:")
    bot.register_next_step_handler(sent, get_info_ru)

    # INFO GET


def get_info_ru(m):
    cid = m.chat.id
    src = m.text
    # print(src)
    r = requests.get('https://bildilchin.az:8888/bildilchin/get/description?selectedWord=' + str(src) + '&indexLang=ru')
    r = r.json()
    if len(r) > 0:
        for word in r:
            a = word["description"]
            a = html2text.html2text(a)
            # print(a)
            bot.send_chat_action(cid, 'typing')
            bot.send_message(cid, "Результаты поиска для: " + str(src))
            if len(a) > 4096:
                for x in range(0, len(a), 4096):
                    bot.send_message(cid, a[x:x + 4096])
            else:
                bot.send_message(cid, a)
            bot.send_message(cid, "Нажмите /start или /RU для нового поиска!")
            break
    else:
        bot.send_message(cid,
                         "Слово, которое вы ищете, не найдено! Используйте команду /start или /RU, чтобы найти новое "
                         "слово!")


@bot.message_handler(commands=["EN"])
def src_en(m):
    cid = m.chat.id
    sent = bot.send_message(cid, "Enter the word you want to find: ")
    bot.register_next_step_handler(sent, get_info_en)

    # INFO GET


def get_info_en(m):
    cid = m.chat.id
    src = m.text
    # print(src)
    r = requests.get('https://bildilchin.az:8888/bildilchin/get/description?selectedWord=' + str(src) + '&indexLang=en')
    r = r.json()
    if len(r) > 0:
        for word in r:
            a = word["description"]
            a = html2text.html2text(a)
            # print(a)
            bot.send_chat_action(cid, 'typing')
            bot.send_message(cid, " Search Results for: " + str(src))
            if len(a) > 4096:
                for x in range(0, len(a), 4096):
                    bot.send_message(cid, a[x:x + 4096])
            else:
                bot.send_message(cid, a)
            bot.send_message(cid, "Press /start or /EN for a new search!")
            break
    else:
        bot.send_message(cid,
                         "The word you are looking for is not found! Use the /start or /EN command to find a new word!")


@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note",
                                    "voice", "location", 'contact', "new_chat_members", "left_chat_member",
                                    "new_chat_title", "new_chat_photo", "delete_chat_photo", "group_chat_created",
                                    "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                                    "migrate_from_chat_id", "pinned_message", "charmap" ])
def send_error(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, "Göndərdiyinizi anlamadım!")
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, "Zəhmət olmasa axtarış dilini seçin: /AZ , /RU , /EN")
    # time.sleep(5)





if __name__ == '__main__':
    try:
        bot.polling()
    except Exception:
        pass


# bot.polling()
