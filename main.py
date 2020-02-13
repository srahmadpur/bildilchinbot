import simplejson
import telebot
import requests
import html2text
import logging
import time

logging.basicConfig(level=logging.ERROR, filename="sys.log")


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if m.content_type == 'text' or "pinned_message":
            # print the sent message to the console and save to file
            t = time.localtime()
            current_time = time.strftime("%d %b %Y %H:%M:%S", t)
            print(str(current_time) + " " + str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + str(m.text))
            f = open("UH.log", 'a', encoding='utf-8')
            f.write(
                str(current_time) + " " + str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + str(m.text) + "\r")
            f.close()


token = '1067624262:AAFc9eePf55C7BapCDhCVFr8qaG09OtyTHw'
bot = telebot.TeleBot(token)
bot.set_update_listener(listener)  # register listener


@bot.message_handler(commands=['start'])
def start_message(m):
    cid = m.chat.id
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Azərbaycan', callback_data="az"))
    markup.add(telebot.types.InlineKeyboardButton(text='Русский', callback_data="ru"))
    markup.add(telebot.types.InlineKeyboardButton(text='English', callback_data="en"))
    bot.send_message(cid, text="Zəhmət olmasa axtarış dilini seçin!", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text='Bildilçin, Sizin üçün axtarar! ')
    answer = ''
    if call.data == 'az':
        answer = "Axtarmaq istədiyiniz sözü daxil edin: "

        @bot.message_handler(content_types="text")
        def get_info_az(m):
            cid = m.chat.id
            src = m.text
            url = 'https://bildilchin.az:8888/bildilchin/get/description?selectedWord=' + str(src) + '&indexLang=az'
            try:
                r = requests.get(url)
                try:
                    r = r.json()
                    if len(r) > 0:
                        for word in r:
                            a = word["description"]
                            a = html2text.html2text(a)
                            bot.send_chat_action(cid, 'typing')
                            bot.send_message(cid, str(src) + "  - sözünə əsasən axtarış nəticələri: ")
                            if len(a) > 4096:
                                for x in range(0, len(a), 4096):
                                    bot.send_message(cid, a[x:x + 4096])
                            else:
                                bot.send_message(cid, a)
                                bot.send_message(cid,
                                                 "Yeni sözü daxil edin və ya axtarış dilini dəyişmək üçün /start "
                                                 "komandasından istifadə edin!")
                            break
                    else:
                        bot.send_message(cid,
                                         "Axtardığınız söz tapılmadı! Yeni sözü daxil edin və ya axtarış dilini "
                                         "dəyişmək üçün /start komandasından istifadə edin! ")
                except simplejson.errors.JSONDecodeError:
                    bot.send_sticker(cid, "CAACAgIAAxkBAAILTF5FEjDaUtAO2n0qlhh9ZfDkcv_oAAJFAAMh8AQcVEccChUEGqEYBA")
                    bot.send_message(cid, "Mən yalnız sözləri axtara bilirəm.")
                    pass
            except requests.exceptions.RequestException:  # This is the correct syntax
                bot.send_message(cid, "Xəta baş verdi. Zəhmət olmasa bir az sonra yenə cəhd edin.")


    elif call.data == 'ru':
        answer = 'Введите слово, которое вы хотите найти: '

        @bot.message_handler(content_types="text")
        def get_info_ru(m):
            cid = m.chat.id
            src = m.text
            url = 'https://bildilchin.az:8888/bildilchin/get/description?selectedWord=' + str(src) + '&indexLang=ru'
            try:
                r = requests.get(url)
                try:
                    r = r.json()
                    if len(r) > 0:
                        for word in r:
                            a = word["description"]
                            a = html2text.html2text(a)
                            bot.send_chat_action(cid, 'typing')
                            bot.send_message(cid, "Результаты поиска для:  " + str(src))
                            if len(a) > 4096:
                                for x in range(0, len(a), 4096):
                                    bot.send_message(cid, a[x:x + 4096])
                            else:
                                bot.send_message(cid, a)
                                bot.send_message(cid,
                                                 "Введите новое слово или используйте команду /start чтобы изменить "
                                                 "язык поиска! ")
                            break
                    else:
                        bot.send_message(cid, "Слово, которое вы ищете, не найдено! Введите новое слово или "
                                              "используйте команду /start чтобы изменить язык поиска.")
                except simplejson.errors.JSONDecodeError:
                    bot.send_sticker(cid, "CAACAgIAAxkBAAILTF5FEjDaUtAO2n0qlhh9ZfDkcv_oAAJFAAMh8AQcVEccChUEGqEYBA")
                    bot.send_message(cid, "Я могу искать только слова.")
                    pass

            except requests.exceptions.RequestException:  # This is the correct syntax
                bot.send_sticker(cid, "CAACAgIAAxkBAAILTF5FEjDaUtAO2n0qlhh9ZfDkcv_oAAJFAAMh8AQcVEccChUEGqEYBA")
                bot.send_message(cid, "Произошла ошибка. Пожалуйста, попробуйте позже.")


    elif call.data == 'en':
        answer = 'Enter the word you want to find: '

        @bot.message_handler(content_types="text")
        def get_info_en(m):
            cid = m.chat.id
            src = m.text
            url = 'https://bildilchin.az:8888/bildilchin/get/description?selectedWord=' + str(src) + '&indexLang=en'
            try:
                r = requests.get(url)
                try:
                    r = r.json()
                    if len(r) > 0:
                        for word in r:
                            a = word["description"]
                            a = html2text.html2text(a)
                            bot.send_chat_action(cid, 'typing')
                            bot.send_message(cid, "Search results for:" + str(src))
                            if len(a) > 4096:
                                for x in range(0, len(a), 4096):
                                    bot.send_message(cid, a[x:x + 4096])
                            else:
                                bot.send_message(cid, a)
                                bot.send_message(cid, "Enter a new word or use the /start command to change the "
                                                      "search language!")
                            break
                    else:
                        bot.send_message(cid, "The word you are looking for not found! Enter a new word or use the "
                                              "/start command to change the language.")
                except simplejson.errors.JSONDecodeError:
                    bot.send_sticker(cid, "CAACAgIAAxkBAAILTF5FEjDaUtAO2n0qlhh9ZfDkcv_oAAJFAAMh8AQcVEccChUEGqEYBA")
                    bot.send_message(cid, "I can only search for words.")
                    pass

            except requests.exceptions.RequestException:  # This is the correct syntax
                bot.send_sticker(cid, "CAACAgIAAxkBAAILTF5FEjDaUtAO2n0qlhh9ZfDkcv_oAAJFAAMh8AQcVEccChUEGqEYBA")
                bot.send_message(cid, "Oops.. Something went wrong. Please try again later..")

    bot.send_message(call.message.chat.id, answer)


@bot.message_handler(content_types=["audio", "emoji", "document", "photo", "sticker", "video", "video_note",
                                    "voice", "location", 'contact', "new_chat_members", "left_chat_member",
                                    "new_chat_title", "new_chat_photo", "delete_chat_photo", "group_chat_created",
                                    "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                                    "migrate_from_chat_id", "pinned_message", "charmap"])
def send_error(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, "Göndərdiyinizi anlamadım!")
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, "Yeni sözü daxil edin və ya axtarış dilini dəyişmək üçün /start komandasından istifadə edin!")
    bot.send_sticker(cid, "CAACAgIAAxkBAAILUl5FLxlYCZ6mgFVBj4kGfGUGu6QTAAJYAAMh8AQcItiUEZ80L8UYBA")
    # time.sleep(5)



if __name__ == '__main__':
    try:
        bot.polling()
    except Exception:
        pass
