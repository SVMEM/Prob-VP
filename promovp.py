import csv
import time
import telebot

token = 'YOURTOKEN'
bot = telebot.TeleBot(token)

with open('nicks.csv', 'r') as fin:
    rid = csv.reader(fin)
    for row in rid:
        idd = row[0]
        # tst = row[3]
        # z1 = 0
        # cz1 = ''
        # z2 = 0
        # cz2 = ''
        # z3 = 0
        # cz3 = ''
        # with open('riiiii.csv', 'r') as fini:
        #     riid = csv.reader(fini)
        #     for roow in riid:
        #         if int(roow[8]) == int(idd):
        #             z1 = roow[1]
        #             cz1 = roow[2]
        #             z2 = roow[3]
        #             cz2 = roow[4]
        #             z3 = roow[5]
        #             cz3 = roow[6]

        text1 = 'Хочешь подготовиться ко Всеросу и затащить диплом всего за 5 недель? 🎓 ' \
                '\n\nТогда экспресс-интенсив к заключительному этапу Всероссийской олимпиады школьников от экономического Олимпа — это именно то, что тебе нужно!' \
                '\n\nВсего за 3400 ты сможешь пройти 6 тем в онлайн режиме и просмотреть еще 3 темы в записи 🔥' \
                '\n\nВ конце интенсива все участники напишут пробную олимпиаду в формате заключительного этапа Всероса.' \
                '\n\nКроме того, ты можешь усиленно заниматься макроэкономикой на Интенсиве с макрой. Он включает в себя все материалы необходимые для подготовки к макроэкономическим задачам на заключительном этапе!' \
                '\n\nПолезные ссылки:' \
                '\n1. Сайт интенсива: https://olymp.education/express_zakl_2024' \
                '\n2. Подключиться к интенсиву с макрой: https://olymp.education/express_s_makro' \
                '\n3. Подключиться к интенсиву без макры: https://olymp.education/express_bez_macro'
        try:
            bot.send_message(idd, text1)
        except:
            True
        else:
            time.sleep(0.2)
