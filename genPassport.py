import random
import sqlite3
import uuid

# Отдельный файл для экспериментов с генерацией серии и номера документа
#con = sqlite3.connect('documents.db')

#cursor = con.cursor()
#cursor.execute("create table documents(id integer primary key, type integer, series text, number text, usage integer default 0)")

def genPassport():
    # для рандома
    randSer2 = str(random.randint(1, 99))
    series = str(random.randint(10, 80)) + ' ' + '0' * (2 - len(randSer2)) + randSer2
    number = str(random.randint(1, 999999))
    number = '0' * (6 - len(number)) + number
    print('%s %s' % (series, number))

    # Для генерации
    # for i in range(44, 46):
    #     for j in range(1, 100):
    #         x = 0
    #         for jj in range(1, 1000000):
    #             number = '0'*(6 - len(str(jj))) + str(jj)
    #             series = str(i) + ' ' + '0' * (2 - len(str(j))) + str(j)
    #             # print(series + ' ' + number)
    #             x += 1
    #             cursor.execute(
    #                 "insert into documents (type, series, number) VALUES ('%s', '%s', '%s')" % (0, series, number))
    #         con.commit()
    #         print('%i: %i' % (j, x))

def genBirthCert():
    alphabet = 'АВЕКМНОРСТХ'
    series = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
    # for s in series:
    #     for a in alphabet:
    #         print('%s-Т%s' % (s, a))

    number = str(random.randint(1, 999999))
    number = '0' * (6 - len(number)) + number

    print('%s-T%s %s' % (series[random.randint(0, 9)], alphabet[random.randint(0, 10)], number))

genPassport()
genBirthCert()