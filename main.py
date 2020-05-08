import telebot
import config
import search_parser as sp
from search_parser import word_info, word_list
import time
import logging


logging.basicConfig(level=logging.INFO, filename="sys.log")


knownUsers = []
userStep = {}


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


bot = telebot.TeleBot(config.token)
bot.set_update_listener(listener)  # register listener



@bot.message_handler(commands=['start'])
def start_message(m):
    cid = m.chat.id
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Azərbaycan', callback_data="az"))
    markup.add(telebot.types.InlineKeyboardButton(text='Русский', callback_data="ru"))
    markup.add(telebot.types.InlineKeyboardButton(text='English', callback_data="en"))
    if cid not in knownUsers:
        knownUsers.append(cid)
        userStep[cid] = ""
        bot.send_message(cid, text=config.Lang_chose_az, reply_markup=markup)
    else:
        bot.send_message(cid, text=config.Query_handler["fa_{}".format(userStep[cid])])
        


@bot.message_handler(commands=["lang"])
def change_lang(m):
    cid = m.chat.id
    markup = telebot.types.InlineKeyboardMarkup()
    markup.add(telebot.types.InlineKeyboardButton(text='Azərbaycan', callback_data="az"))
    markup.add(telebot.types.InlineKeyboardButton(text='Русский', callback_data="ru"))
    markup.add(telebot.types.InlineKeyboardButton(text='English', callback_data="en"))
    if cid not in knownUsers:
        knownUsers.append(cid)
        bot.send_message(cid, text=config.Lang_chose_az, reply_markup=markup)
    else:
        bot.send_message(cid, text=config.Lang_chose_az, reply_markup=markup)




@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    bot.answer_callback_query(callback_query_id=call.id, text=config.Query_handler["hello_msg"])
    first_answer = ''
    if call.data == 'az':
        cd = call.data
        userStep.update({call.message.chat.id: cd})
        first_answer = config.Query_handler["fa_az"]
    elif call.data == 'ru':
        cd = call.data
        userStep.update({call.message.chat.id: cd})
        first_answer = config.Query_handler["fa_ru"]
    elif call.data == 'en':
        cd = call.data
        userStep.update({call.message.chat.id: cd})
        first_answer = config.Query_handler["fa_en"]
    bot.send_message(call.message.chat.id, first_answer)



@bot.message_handler(func=lambda message: True)
def word_search(message):
    cid = message.chat.id
    if cid not in knownUsers:
        knownUsers.append(cid)
        userStep.update({cid:""})
        bot.send_message(message.chat.id, text=config.lang_not_chsn)
        #"New user detected, who hasn't used \"/start\" yet"
    else:
        cd = userStep[cid]
        if str(message.text) == "None":
            bot.send_sticker(message.chat.id, config.none_text["none_scr_id"])
            bot.send_message(message.chat.id, text= config.none_text[("none_{}".format(cd))])
        else:
            second_answer = sp.dict_search(word=message.text, lang= cd)
            if second_answer == "Word_Not_Found":
                second_answer = config.No_Word[("no_{}".format(cd))]
                bot.send_message(message.chat.id, second_answer)
            else:
                bot.send_message(message.chat.id, "{0} {1}".format(config.Yes_Word["yes_{}".format(cd)] , message.text))
                for element in second_answer:
                    bot.send_message(message.chat.id, "<b>" + element.dict_name + "</b>", parse_mode="HTML")
                    if len(element.w_info) > 4096:
                        for x in range(0, len(element.w_info), 4096):
                            bot.send_message(message.chat.id, element.w_info[x:x + 4096])
                    else:
                        bot.send_message(message.chat.id, element.w_info)
                bot.send_message(message.chat.id, text= config.New_Word[("new_{}".format(cd))])
                word_list.clear()
                cd = ""



if __name__ == '__main__':
    try:
        bot.polling()
    except Exception:
        pass

