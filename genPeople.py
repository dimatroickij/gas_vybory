import random
from datetime import datetime, timedelta

from mimesis import Person
from mimesis.enums import Gender

# таблица настройки, увеличенная до 150_000_000
# count = 150_000_000
# capacity = 110_000_000
# no_capacity = 7_650_000
# детей = 32_350_000: 0-13= 24_408_705, 14-17: 7_941_295
# мужчин = 68_855_000
# женчин = 81_145_000

# Типы УИП:
# 1) Дети 0 - 13 лет
# 1.a) мужской пол: 11_228_000 (gender=1, ageMin=0, ageMax=13, capacity=1, doc_code=?)
# 1.б) женский пол: 13_180_701 (gender=2, ageMin=0, ageMax=13, capacity=1, doc_code=?)
# 2) Дети 14 - 17 лет:
# 2.а) мужской пол: 3_652_996 (gender=1, ageMin=14, ageMax=17, capacity=1, doc_code=10)
# 2.б) женский пол: 4_288_299 (gender=2, ageMin=14, ageMax=17, capacity=1, doc_code=10)
# 3) Взрослые 18 - ..., дееспособные
# 3.а) мужской пол: 50_600_000 (gender=1, ageMin=18, ageMax=90, capacity=1, doc_code=10)
# 3.б) женский пол: 59_400_000 (gender=2, ageMin=18, ageMax=90, capacity=1, doc_code=10)
# 4) Взрослые 18 - .., недееспособные
# 4.а) мужской пол: 3_520_000 (gender=1, ageMin=18, ageMax=90, capacity=2, doc_code=10)
# 4.б) женский пол: 4_130_000 (gender=2, ageMin=18, ageMax=90, capacity=2, doc_code=10)

def gen_datetime(ageMin, ageMax):
    start = datetime(2020 - ageMin, datetime.now().month, datetime.now().day, 00, 00, 00)
    end = datetime(2020 - ageMax - 1, datetime.now().month, datetime.now().day, 00, 00, 00) + timedelta(days=20)
    # Проверить, почему вылетает ошибка при большой разнице возрастов
    date3 = int(end.timestamp())
    date2 = int(start.timestamp()) - date3
    date1 = random.randint(0, date2)
    return datetime.fromtimestamp(end.timestamp() + date1)

def gen_doc_issue_date(birth):
    age = int((datetime.now() - birth).days / 365.2425)

    if age < 14:
        return birth + timedelta(days=10)
    elif age >= 14 and age < 20:
        return birth + timedelta(days=14 * 365 + 4 + 15)  # 4 - возможное количество високосных годов
    elif age >= 20 and age < 45:
        return birth + timedelta(days=20 * 365 + 5 + 15)  # 5 - возможное количество високосных годов
    else:
        return birth + timedelta(days=458365 + 12 + 15)  # 12 - возможное количество високосных годов

def gen_doc_number(type):
    if type == 0:
        randSer2 = str(random.randint(1, 99))
        series = str(random.randint(10, 80)) + ' ' + '0' * (2 - len(randSer2)) + randSer2
        number = str(random.randint(1, 999999))
        number = '0' * (6 - len(number)) + number
    elif type == 1:
        alphabet = 'АВЕКМНОРСТХ'
        romanNum = ['I', 'II', 'III', 'IV', 'V', 'VI', 'VII', 'VIII', 'IX', 'X']
        number = str(random.randint(1, 999999))
        number = '0' * (6 - len(number)) + number
        series = romanNum[random.randint(0, 9)] + '-T' + alphabet[random.randint(0, 10)]
    else:
        number = ''
        series = ''
    return [series, number]

class UIP:
    def __init__(self, sys_elector_id, gender, ageMin, ageMax, capacity):
        # Словарь пола
        genderList = {1: Gender.MALE, 2: Gender.FEMALE}
        # Суффиксы отчества в зависимоти от пола
        genderSuffix = {1: 'ович', 2: 'овна'}
        #Словарь типов документа
        docList = {0:[10,9], 1:[123456789,5]}
        person = Person('ru')

        #Генерация даты рождения в завсимости от возраста
        birth = gen_datetime(ageMin, ageMax)

        #Данные для таблицы elector
        self.elector_id = None # PK из таблицы
        self.last_name = person.last_name(gender=genderList[gender])
        self.first_name = person.first_name(gender=genderList[gender])
        self.middle_name = person.first_name(gender=genderList[gender]) + genderSuffix[gender]
        self.birth_day = birth.strftime('%Y-%m-%d')
        self.birth_day_string = birth.strftime('%Y.%m.%d')
        self.gender_id = gender
        self.capacity_id = capacity
        self.country_id = 643
        self.start_date = birth.strftime('%Y-%m-%d') + ' 00:00:00' #для таблицы elector
        #НЕТ ИНФОРМАЦИИ О СПОСОБЕ ГЕНЕРАЦИИ ПОЛЯ (пока приходит готовое) sys_elector_id
        self.sys_elector_id = sys_elector_id
        self.address_id = 1

        # Данные для таблицы elector_doc
        self.elector_doc_id = None # PK из таблицы
        #НЕПОНЯТНО КАК МЕНЯТЬ (ТАК КАК У КАЖДОГО УИП СВОЕ МЕСТО ВЫДАЧИ ДОКУМЕНТА). Сейчас одинаковое значение:
        self.subject_global_id = 123

        if ageMax < 14:
            doc_code = 1
        else:
            doc_code = 0
        self.elector_doc_code_id = docList[doc_code][0]
        doc_data = gen_doc_number(doc_code)
        self.elect_doc_series = doc_data[0]
        self.elect_doc_number = doc_data[1]
        self.start_date2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S') #для таблицы elector_doc

        self.elect_doc_issue_date = gen_doc_issue_date(birth).strftime('%Y-%m-%d')
        self.elector_doc_type_id = docList[doc_code][1]

        # Данные для таблицы elector_residence
        self.elector_residence_id = None # PK из таблицы
        self.elector_residence_kind_id = 1
        #НЕПОНЯТНО КАК МЕНЯТЬ (ТАК КАК У КАЖДОГО УИП СВОЕ МЕСТО ЖИТЕЛЬСТВА). Сейчас постоянное значение
        self.residence_address_id = 111111111

        # Данные для таблицы elector_change_log
        #НЕИЗВЕСТНО ЗНАЧЕНИЕ, но вроде везде 1
        self.change_type_id = 1
        self.change_number = 0
        self.change_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d %H:%M:%S')
        self.change_basis_id = 89 # 89 - листок прибытия, 85 - рождение, 97 - листок убытия
        self.kca = 1
        #БУДЕТ БРАТЬСЯ ИЗ ID СОЗДАННОГО person: self.elector_id = ''
        #БУДЕТ БРАТЬСЯ ИЗ ID СОЗДАННОГО документа self.elector_doc_id
        #БУДЕТ БРАТЬСЯ ИЗ ID СОЗДАННОГО elector_residence self.elector_residence_id

        #input_source = 1
        self.input_source = 1

    def getElector(self):
        return [self.last_name, self.first_name, self.middle_name, self.birth_day, self.birth_day_string,
                self.gender_id, self.capacity_id, self.country_id, self.start_date, self.input_source,
                self.sys_elector_id, self.address_id]

    def setElector_id(self, elector_id):
        self.elector_id = elector_id

    def getElector_kind(self):
        return [self.sys_elector_id, self.start_date2, '[{"id": 1}]']

    def getElector_doc(self):
        return [self.sys_elector_id, self.subject_global_id, self.elector_doc_code_id, self.elect_doc_series,
                self.elect_doc_number, self.input_source, self.start_date2, self.elect_doc_issue_date,
                self.elector_doc_type_id]

    def setElector_doc_id(self, elector_doc_id):
        self.elector_doc_id = elector_doc_id

    def getElector_residence(self):
        return [self.sys_elector_id, self.residence_address_id, self.input_source, self.elector_residence_kind_id,
                self.start_date2[0:10] + ' 00:00:00']

    def setElector_residence_id(self, elector_residence_id):
        self.elector_residence_id = elector_residence_id

    def getElector_change_log(self):
        return [self.elector_id, self.elector_doc_id, self.elector_residence_id, self.sys_elector_id,
                self.change_type_id, self.change_number, self.change_date, self.start_date2, self.kca,
                self.change_basis_id, self.input_source]

# Нужно генерировать sys_elector_id; брать из БД subject_global_id, residence_address_id
# people = UIP(sys_elector_id=123456789, gender=1, ageMin=18, ageMax=50, capacity=1)
# print(people.getElector())
# #people.setElector_id(123456)
# print(people.getElector_king())
# print(people.getElector_doc())
# #people.setElector_doc_id('000000')
# print(people.getElector_residence())
# #people.setElector_residence_id()
# print(people.getElector_change_log())