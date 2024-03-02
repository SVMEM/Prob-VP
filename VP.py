import telebot
from telebot import types
import datetime
import pendulum
import csv
token = 'YOURTOKEN'
bot = telebot.TeleBot(token)


markup = types.ReplyKeyboardMarkup()
btn1 = types.KeyboardButton('Сдать задачи')
btn2 = types.KeyboardButton('Завершить')
markup.row(btn1, btn2)



markupn = types.ReplyKeyboardMarkup()
btn1 = types.KeyboardButton('Назад')
markupn.row(btn1)

markupyn = types.ReplyKeyboardMarkup()
btn1 = types.KeyboardButton('да')
btn2 = types.KeyboardButton('нет')
markupyn.row(btn1, btn2)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет, команда ВЭШ рада приветствовать тебя на нашем пробном заключительном этапе"
                                      " Высшей Пробы! \n\nМы очень надеемся, что тебе понравятся задачи, которые мы подготовили "
                                      "для тебя! Для начала давай создадим уникальный никнейм. По нему ты сможешь"
                                      " узнать свое место в рейтинге среди написавших. Если ты не хочешь, чтобы твой"
                                      " результат увидели другие участники, ты всегда можешь создать случайный ник,"
                                      " по которому никто не сможет тебя идентифицировать (например romasavin2005)."
                                      " Все оскорбительные никнеймы будут удалены.\nВ случае возникновения технических"
                                      " неполадок используй /help. Если это не помогло решить проблему,"
                                      " напиши Роме (@raamensavin).")
    bot.register_next_step_handler(message, nick)


def nick(message):
    if message.text[0] == '/' or len(message.text) > 30:
        bot.send_message(message.chat.id, "Некорректное имя попробуйте другое")
        bot.register_next_step_handler(message, nick)
    else:
        a = 0
        with open('nicks.csv', "r") as fin:
            re = csv.reader(fin)
            at = []
            for row in re:
                at += row
            if at.count(message.text) != 0:
                bot.send_message(message.chat.id, "Занят, выберите другой")
                bot.register_next_step_handler(message, nick)
            else:
                a = 1
        if a == 1:
            with open('nicks.csv', "a") as fin:
                writer = csv.writer(fin)
                usr = [message.from_user.id, message.from_user.username, message.text]
                writer.writerow(usr)
                bot.send_message(chat_id='YOURCHATID', text=f"{message.from_user.username} зарегался как {message.text}")
                #bot.send_document(message.chat.id, open('Пробный Муницип.pdf', "rb"))
                msg = bot.send_message(message.chat.id, f"Очень приятно, {message.text}, для продолжения укажи, "
                                                        f"пожалуйста, свою фамилию.")
                bot.register_next_step_handler(msg, fio)


def fio(message):
    if not message.text.isalpha():
        bot.send_message(message.chat.id, 'Какая-то проблема в формате, попробуй перечитать инструкцию к формату.')
        bot.register_next_step_handler(message, fio)
    else:
        with open('imena.csv', "a") as fin:
            writer = csv.writer(fin)
            ussr = message.text.split(',') + [f'{message.from_user.username}']
            writer.writerow(ussr)
        bot.send_message(message.chat.id, 'Супер, все готово, для приступления к сдаче задач используй /pognali.\n'
                                          'Сразу после отправки команды пойдет время, а именно 200 минут на решение за'
                                          'дачек и 10 минут на загрузку, всего 210 минут. По истечении данного време'
                                          'ни возможности сдать задания не будет.')


@bot.message_handler(commands=['pognali'])
def ziza(message):
    a = 0
    with open('time.csv', 'r') as fin:
        rid = csv.reader(fin)
        for row in rid:
            if int(row[0]) == int(message.from_user.id):
                a = 1
    if a == 0:
        bot.send_document(message.chat.id, open('vpvpv.pdf', "rb"))
        with open('time.csv', 'a') as fin:
            writer = csv.writer(fin)
            usr = [message.from_user.id, message.from_user.username, datetime.datetime.now()+datetime.timedelta(minutes=210)]
            writer.writerow(usr)
        bot.send_message(message.chat.id, text=f'Сейчас - {pendulum.now("Europe/Moscow").format("HH:mm:ss")}, конец - {(pendulum.now("Europe/Moscow").add(minutes=210)).format("HH:mm:ss")}'
                                               f'\n\n\nВыберите часть:', reply_markup=markup)
        bot.register_next_step_handler(message, click)
    else:
        bot.send_message(message.chat.id, 'Вы уже начали, выберите часть:', reply_markup=markup)
        bot.register_next_step_handler(message, click)


def click(message):
    if message.text.lower() == 'сдать задачи':
        msg = bot.send_message(message.chat.id, 'Пришлите ОДИН pdf файл с вашим решением задач, файлы разбитые на нес'
                                                'колько фотографий или документов или в другом формате'
                                                ' обработаны не будут и, к сожалению, мы не сможем'
                                                ' их проверить. Для создания одного файла можно использовать онлайн сер'
                                                'висы, такие как ilovepdf.com.', reply_markup=markupn)
        bot.register_next_step_handler(msg, ch4)
    elif message.text.lower() == 'завершить':
        a = 1
        if a == 0:
            bot.send_message(message.chat.id, 'Вы не сдали ни одной задачи')
            bot.register_next_step_handler(message, click)
        else:
            msg = bot.send_message(message.chat.id, 'Вы уверены, что хотите закончить?', reply_markup=markupyn)
            bot.register_next_step_handler(msg, check)
    else:
        msg = bot.send_message(message.chat.id, 'Используйте кнопки')
        bot.register_next_step_handler(msg, click)


def check(message):
    if message.text.lower() == 'да':
        bot.send_message(message.chat.id, 'Понравилось? Присоединяйся к другим нашим проектам: \n1. Воскресным контестам'
                                          ' от ВЭШ, которые ты можешь найти по ссылке: https://t.me/contest_vesh \n2. '
                                          'Нашему интенсиву к заключительным этапам олимпиад по Экономике, в том числе и к Высшей Пробе. '
                                          'Больше информации можно найти по ссылке:'
                                          ' https://olymp.education/intensive_zakl_2024. А также следи за'
                                          ' результатами в наших социальных сетях!\n\n Не спеши блокировать бота, ведь'
                                          'через него же мы отправим баллы и фидбэк.'
                                          ' До скорых встреч!', reply_markup=types.ReplyKeyboardRemove())
    elif message.text.lower() == 'нет':
        bot.send_message(message.chat.id, text='Выберите часть:', reply_markup=markup)
        bot.register_next_step_handler(message, click)
    else:
        bot.send_message(message.chat.id, text='Что-то не так, используйте кнопки.', reply_markup=markupyn)
        bot.register_next_step_handler(message, check)


def ch4(message):
    with open('time.csv', 'r') as fin:
        rid = csv.reader(fin)
        for row in rid:
            if int(row[0]) == int(message.from_user.id):
                titi = datetime.datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S.%f')
    if datetime.datetime.now() > titi:
        bot.send_message(message.chat.id, 'Время вышло, отправленные ответы обработаны, но новые отправить нельзя.')
    else:
        if message.photo is not None:
            msg1 = bot.send_message(message.chat.id, 'Это фотография а не файл, отправьте файл.', reply_markup=markupn)
            bot.register_next_step_handler(msg1, ch4)
        elif message.document is not None:
            if message.document.file_name.endswith('.pdf'):
                bot.forward_message('YOURCHATID', message.chat.id, message.message_id)
                bot.send_message(chat_id='YOURCHATID', text=f"{message.from_user.username} {message.from_user.id} сдал")
                bot.send_message(message.chat.id, 'Принято, для того, чтоб отправить другой файл выберите эту часть еще раз'
                                                  ', проверен будет только последний отправленный файл. Вы можете выбра'
                                                  'ть другую часть или завершить работу.', reply_markup=markup)
                bot.register_next_step_handler(message, click)
            else:
                msg1 = bot.send_message(message.chat.id, 'Это не pdf, попробуйте еще раз', reply_markup=markupn)
                bot.register_next_step_handler(msg1, ch4)
        else:
            if message.text.lower() == 'назад':
                bot.send_message(message.chat.id, text='Выберите часть:', reply_markup=markup)
                bot.register_next_step_handler(message, click)
            else:
                msg1 = bot.send_message(message.chat.id, 'Это не файл, отправьте решение все развернутые решения 4 части'
                                                         ' одним файлом', reply_markup=markupn)
                bot.register_next_step_handler(msg1, ch4)
    
@bot.message_handler(commands=['help'])
def help_m(message):
    bot.send_message(message.chat.id, 'После создания ника и заполнения ваших данных, вы должны были получить файл с за'
                                      'даниями, если этого не произошло, свяжитесь с Ромой @raamensavin. После получения'
                                      ' задач используйте /region для сдачи ответов. Внимательно прочитайте инструкцию по'
                                      'формату ответов и всем удачи!!')


bot.infinity_polling()
