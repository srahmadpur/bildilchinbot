import telebot
import requests
import html2text
import logging
import time

logging.basicConfig(level=logging.ERROR, filename="my.log")

def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        if not m.content_type != 'text' or "pinned_message":
            # print the sent message to the console
            t = time.localtime()
            current_time = time.strftime("%d %b %Y %H:%M:%S", t)
            print(str(current_time) + " " + str(m.chat.first_name) + " [" + str(m.chat.id) + "]: " + str(m.text))



bot = telebot.TeleBot("1067624262:AAFc9eePf55C7BapCDhCVFr8qaG09OtyTHw")
bot.set_update_listener(listener)  # register listener


@bot.message_handler(commands=["start"])
def send_echo(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, "Bildilçinə xoş gəldin!")
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, "Zəhmət olmasa axtarış dilini seç: /az /ru /en")




@bot.message_handler(commands=["az"])
def src_az(m):
    cid = m.chat.id
    sent = bot.send_message(cid, "Axtarmaq istədiyiniz sözü daxil edin:")
    bot.register_next_step_handler(sent, get_info_az)
    # INFO GET

def get_info_az(m):
    cid = m.chat.id
    src = m.text
    url = 'https://bildilchin.az:8888/bildilchin/get/description?selectedWord=' + str(src) + '&indexLang=az'
    try:
        r = requests.get(url)
        r = r.json()
        if len(r) > 0:
            for word in r:
                a = word["description"]
                a = html2text.html2text(a)
                bot.send_chat_action(cid, 'typing')
                bot.send_message(cid, str(src) + "  -sözünə əsasən axtarış nəticələri: ")
                if len(a) > 4096:
                    for x in range(0, len(a), 4096):
                        bot.send_message(cid, a[x:x + 4096])
                else:
                    bot.send_message(cid, a)
                bot.send_message(cid, "Yeni söz axtarmaq üçün /az /ru /en komandalarından istifadə et!")
                break
        else:
            bot.send_message(cid,
                     "Axtardığınız söz tapılmadı! Yeni söz axtarmaq üçün /az /ru /en komandalarından istifadə "
                     "et!")
    except requests.exceptions.RequestException:  # This is the correct syntax
        bot.send_message(cid, "Xəta baş verdi. Zəhmət olmasa bir az sonra yenə cəhd edin.")



@bot.message_handler(commands=["ru"])
def src_ru(m):
    cid = m.chat.id
    sent = bot.send_message(cid, "Введите слово, которое вы хотите найти:")
    bot.register_next_step_handler(sent, get_info_ru)
    # INFO GET

def get_info_ru(m):
    cid = m.chat.id
    src = m.text
    url = 'https://bildilchin.az:8888/bildilchin/get/description?selectedWord=' + str(src) + '&indexLang=ru'
    try:
        r = requests.get(url)
        r = r.json()
        if len(r) > 0:
            for word in r:
                a = word["description"]
                a = html2text.html2text(a)
                bot.send_chat_action(cid, 'typing')
                bot.send_message(cid, "Результаты поиска для: " + str(src))
                if len(a) > 4096:
                    for x in range(0, len(a), 4096):
                        bot.send_message(cid, a[x:x + 4096])
                else:
                    bot.send_message(cid, a)
                bot.send_message(cid, "Нажмите /az /ru /en для нового поиска!")
                break
        else:
            bot.send_message(cid,
                         "Слово, которое вы ищете, не найдено! Используйте команду /az /ru /en , чтобы найти новое "
                         "слово!")
    except requests.exceptions.RequestException:  # This is the correct syntax
        bot.send_message(cid, "Упс! Что-то пошло не так. Пожалуйста, попробуйте позже..")



@bot.message_handler(commands=["en"])
def src_en(m):
    cid = m.chat.id
    sent = bot.send_message(cid, "Enter the word you want to find: ")
    bot.register_next_step_handler(sent, get_info_en)
    # INFO GET

def get_info_en(m):
    cid = m.chat.id
    src = m.text
    url = 'https://bildilchin.az:8888/bildilchin/get/description?selectedWord=' + str(src) + '&indexLang=en'
    try:
        r = requests.get(url)
        r = r.json()
        if len(r) > 0:
            for word in r:
                a = word["description"]
                a = html2text.html2text(a)
                bot.send_chat_action(cid, 'typing')
                bot.send_message(cid, " Search results for: " + str(src))
                if len(a) > 4096:
                    for x in range(0, len(a), 4096):
                        bot.send_message(cid, a[x:x + 4096])
                else:
                    bot.send_message(cid, a)
                bot.send_message(cid, "Press /az /ru /en for a new search!")
                break
        else:
            bot.send_message(cid,
                         "The word you are looking for is not found! Use the /az /ru /en command to find a new word!")
    except requests.exceptions.RequestException:  # This is the correct syntax
        bot.send_message(cid, "Oops.. Something went wrong. Please try again later..")


@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note",
                                    "voice", "location", 'contact', "new_chat_members", "left_chat_member",
                                    "new_chat_title", "new_chat_photo", "delete_chat_photo", "group_chat_created",
                                    "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                                    "migrate_from_chat_id", "pinned_message", "charmap"])
def send_error(m):
    cid = m.chat.id
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, "Göndərdiyinizi anlamadım!")
    bot.send_chat_action(cid, 'typing')
    bot.send_message(cid, "Zəhmət olmasa axtarış dilini seçin: /az /ru /en")
    # time.sleep(5)





if __name__ == '__main__':
    try:
        bot.polling()
    except Exception:
        pass
