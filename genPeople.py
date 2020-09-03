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
    return datetime.fromtimestamp(end.timestamp() + random.randint(0, int(start.timestamp()) - int(end.timestamp())))

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
    pass

class UIP:
    def __init__(self, gender, ageMin, ageMax, capacity, doc_code):
        # Словарь пола
        genderList = {1: Gender.MALE, 2: Gender.FEMALE}
        # Суффиксы отчества в зависимоти от пола
        genderSuffix = {1: 'ович', 2: 'овна'}
        #Словарь типов документа
        docList = {0:[10,9], 1:[1,1]}
        person = Person('ru')

        #Генерация даты рождения в завсимости от возраста
        birth = gen_datetime(ageMin, ageMax)

        #Данные для таблицы elector
        self.last_name = person.last_name(gender=genderList[gender])
        self.first_name = person.first_name(gender=genderList[gender])
        self.middle_name = person.first_name(gender=genderList[gender]) + genderSuffix[gender]
        self.birth_day = birth.strftime('%Y-%m-%d')
        self.birth_day_string = birth.strftime('%Y.%m.%d')
        self.gender_id = gender
        self.capacity_id = capacity
        self.country_id = 643
        self.start_date = birth.strftime('%Y-%m-%d') + ' 00:00:00+03' #для таблицы elector
        self.input_source_id = 1
        #НЕТ ИНФОРМАЦИИ О СПОСОБЕ ГЕНЕРАЦИИ ПОЛЯ        self.sys_elector_id = ''
        self.address_id = 1

        # Данные для таблицы elector_doc
        #НЕПОНЯТНО КАК МЕНЯТЬ (ТАК КАК У КАЖДОГО УИП СВОЕ МЕСТО ВЫДАЧИ ДОКУМЕНТА)        self.subject_id = ''
        self.elector_doc_code_id = docList[doc_code][0]
        self.elect_doc_series = ''
        self.elect_doc_number = ''
        #НЕТ ИНФОРМАЦИИ О ПОЛЕ self.start_date2 = '' #для таблицы elector_doc

        self.elect_doc_issue_date = gen_doc_issue_date(birth).strftime('%Y-%m-%d')
        self.elector_doc_type_id = docList[doc_code][1]
        self.start_date = birth + timedelta(days=20)

        # Данные для таблицы elector_residence
        self.elector_residence_kind_id = 1
        #НЕПОНЯТНО КАК МЕНЯТЬ (ТАК КАК У КАЖДОГО УИП СВОЕ МЕСТО ЖИТЕЛЬСТВА)self.residence_address_id = ''

        # Данные для таблицы elector_change_log
        #НЕИЗВЕСТНО ЗНАЧЕНИЕ self.change_type_id = ''
        self.change_number = 1
        self.change_basis_id = 85
        #БУДЕТ БРАТЬСЯ ИЗ ID СОЗДАННОГО person: self.elector_id = ''
        #БУДЕТ БРАТЬСЯ ИЗ ID СОЗДАННОГО документа self.elector_doc_id
people = UIP(1, 14, 17, 1, 0)
print(people.birth_day + ' ||| ' + people.elect_doc_issue_date)