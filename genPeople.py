import csv
import json
import random
from datetime import datetime, timedelta


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


class UIP:
    def __init__(self, sys_elector_id, gender, ageMin, ageMax, capacity, elector_id, elector_doc_id,
                 elector_residence_id, elector_change_log_id, elector_kind_id):
        self.data = None
        with open("person.json", "r", encoding='UTF-8') as read_file:
            self.data = json.load(read_file)

        # Список адресов регистрации
        self.residence = None
        with open("residence_id.csv", "r", encoding='UTF-8') as read_file:
            residence = csv.reader(read_file, delimiter='|')
            self.residence = list(residence)[0]

        # Список мест выдачи паспорта
        self.subject = None
        with open("subject_id.json", "r", encoding='UTF-8') as subject_file:
            self.subject = json.load(subject_file)

        # Словарь пола
        genderList = {1: 'male', 2: 'female'}
        # Суффиксы отчества в зависимоти от пола
        genderSuffix = {1: 'ович', 2: 'овна'}
        # Словарь типов документа
        docList = {0: ['10', '9'], 1: [None, '5']}

        # Генерация даты рождения в завсимости от возраста
        birth = self.gen_datetime(ageMin, ageMax)

        # Данные для таблицы elector
        # PK из таблицы, но будет устанавливаться вручную, при этом надо поддерживать соответствие с последовательностями из базы
        self.elector_id = elector_id
        self.sys_elector_id = sys_elector_id  # НЕТ ИНФОРМАЦИИ О СПОСОБЕ ГЕНЕРАЦИИ ПОЛЯ (пока приходит готовое) sys_elector_id
        self.last_name = self.gen_surname(genderList[gender])
        self.first_name = self.gen_name(genderList[gender])
        self.middle_name = self.gen_name(genderList[gender]) + genderSuffix[gender]
        self.birth_day = birth.strftime('%Y-%m-%d')
        self.birth_day_string = birth.strftime('%Y.%m.%d')
        self.is_birth_day_year_only = False
        self.gender_id = gender
        self.capacity_id = capacity
        self.address_id = 1
        self.country_id = 643
        self.snils = self.inn = None
        self.start_date = birth.strftime('%Y-%m-%d') + ' 00:00:00'  # для таблицы elector
        self.end_date = None
        self.input_source = 1
        self.is_actual = True
        self.kca = 1
        self.capacity_actual_date = None

        # Данные для таблицы elector_kind
        self.elector_kind_id = elector_kind_id
        # sys_elector_id
        self.create_date = self.start_date2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.elector_kinds_json = json.dumps([{'id': 1}])
        self.has_external_vision = False

        # Данные для таблицы elector_doc
        self.elector_doc_id = elector_doc_id  # надо поддерживать соответствие с последовательностями из базы
        # sys_elector_id
        if ageMax < 14:
            doc_code = 1
        else:
            doc_code = 0
        self.subject_global_id = random.choice(self.subject[str(doc_code)])
        self.elector_doc_code_id = docList[doc_code][0]
        doc_data = self.gen_doc_number(doc_code)
        self.elect_doc_series = doc_data[0]
        self.elect_doc_number = doc_data[1]
        # input_source_id
        # start_date_2
        # self.end_date
        # is_actual
        # kca
        self.elect_doc_issue_date = self.gen_doc_issue_date(birth).strftime('%Y-%m-%d')
        self.elector_doc_type_id = docList[doc_code][1]

        # Данные для таблицы elector_residence
        self.elector_residence_id = elector_residence_id  # PK из таблицы
        # sys_elector_id
        self.residence_address_id = random.choice(self.residence)
        self.arrival_address_id = self.departure_address_id = self.temp_start_date = self.temp_end_date = None
        # input_source
        self.elector_residence_kind_id = 1
        self.start_date3 = self.start_date2[0:10] + ' 00:00:00'
        # end_date
        # is_actual
        # kca
        self.arrive_prefered_date = self.temp_doc_number = None
        self.is_create_arrive_needed = False

        # Данные для таблицы elector_change_log
        self.elector_change_log_id = elector_change_log_id
        # elector_id
        # elector_doc_id
        # elector_residence_id
        self.elector_zags_info_id = None
        # sys_elector_id
        self.change_type_id = 1
        self.change_number = 0
        self.change_date = self.birth_day + ' 00:00:00'
        # is_actual
        # start_date2
        self.create_user_id = None
        # input_source
        # kca
        self.change_basis_id = 85  # 89 - листок прибытия, 85 - рождение, 97 - листок убытия
        self.is_death = False
        self.is_deleted = False
        self.import_log_id = None
        self.is_approved = True
        # start_date2
        self.update_user_id = None
        self.is_departured_in_military = False
        self.is_departured_from_addr = False
        self.is_departured_in_prison = False
        self.kind_names = 'избиратель'

    def gen_datetime(self, ageMin, ageMax):
        start = datetime(2020 - ageMin, datetime.now().month, datetime.now().day, 00, 00, 00)
        end = datetime(2020 - ageMax - 1, datetime.now().month, datetime.now().day, 00, 00, 00) + timedelta(days=20)
        return end + timedelta(days=random.randint(0, (start - end).days))

    def gen_doc_issue_date(self, birth):
        age = int((datetime.now() - birth).days / 365.2425)

        if age < 14:
            return birth + timedelta(days=10)
        elif age >= 14 and age < 20:
            return birth + timedelta(days=14 * 365 + 4 + 15)  # 4 - возможное количество високосных годов
        elif age >= 20 and age < 45:
            return birth + timedelta(days=20 * 365 + 5 + 15)  # 5 - возможное количество високосных годов
        else:
            return birth + timedelta(days=458365 + 12 + 15)  # 12 - возможное количество високосных годов

    def gen_doc_number(srlf, type):
        if type == 0:
            randSer2 = str(random.randint(1, 99))
            series = str(random.randint(10, 80)) + ' ' + '0' * (2 - len(randSer2)) + randSer2
            number = str(random.randint(1, 999999))
            number = '0' * (6 - len(number)) + number
        elif type == 1:
            alphabet = 'АВЕКМНОРСТХ'
            romanNum = ['I', 'V', 'L', 'X', 'C']
            number = str(random.randint(1, 999999))
            number = '0' * (6 - len(number)) + number
            series = romanNum[random.randint(0, 5)] + '-' + alphabet[random.randint(0, 10)] + alphabet[random.randint(0, 10)]
        else:
            number = ''
            series = ''
        return [str(series), str(number)]

    def gen_name(self, sex):
        return random.choice(self.data['names'][sex])

    def gen_surname(self, sex):
        return random.choice(self.data['surnames'][sex])

    def genResidenceAddressFile(self):
        keys = []
        with open('address.csv', 'r', encoding='UTF-8') as address_file:
            csv_people = csv.reader(address_file, delimiter='|')
            for row in csv_people:
                if row[5] == '11':
                    keys.append(row[0])
        with open('residence_id.csv', 'w', encoding='UTF-8') as residence_id_file:
            csv_residence_file = csv.writer(residence_id_file, delimiter='|')
            csv_residence_file.writerow(keys)

    def genSubjectIdFile(self):
        keys = {0: [], 1: []}
        with open('subject.csv', 'r', encoding='UTF-8') as subject_file:
            csv_subject = csv.reader(subject_file, delimiter='|')
            for row in csv_subject:
                if int(row[7]) in [2, 9, 100]:
                    keys[0].append(row[1])
                elif int(row[7]) == 3:
                    keys[1].append(row[1])
        with open('subject_id.json', 'w', encoding='UTF-8') as subject_id_file:
            json.dump(keys, subject_id_file)

    def getElector(self):
        return [self.elector_id, self.sys_elector_id, self.last_name, self.first_name, self.middle_name,
                self.birth_day, self.birth_day_string, self.is_birth_day_year_only, self.gender_id, self.capacity_id,
                self.address_id, self.country_id, self.snils, self.inn, self.start_date, self.end_date,
                self.input_source, self.is_actual, self.kca, self.capacity_actual_date]

    def setElector_id(self, elector_id):
        self.elector_id = elector_id

    def getElector_kind(self):
        return [self.elector_kind_id, self.sys_elector_id, self.create_date, self.elector_kinds_json,
                self.has_external_vision]

    def getElector_doc(self):
        return [self.elector_doc_id, self.sys_elector_id, self.subject_global_id, self.elector_doc_code_id,
                self.elect_doc_series, self.elect_doc_number, self.input_source, self.start_date2, self.end_date,
                self.is_actual, self.kca, self.elect_doc_issue_date, self.elector_doc_type_id]

    def setElector_doc_id(self, elector_doc_id):
        self.elector_doc_id = elector_doc_id

    def getElector_residence(self):
        return [self.elector_residence_id, self.sys_elector_id, self.residence_address_id, self.arrival_address_id,
                self.departure_address_id, self.temp_start_date, self.temp_end_date, self.input_source,
                self.elector_residence_kind_id, self.start_date3, self.end_date, self.is_actual, self.kca,
                self.arrive_prefered_date, self.is_create_arrive_needed, self.temp_doc_number]

    def setElector_residence_id(self, elector_residence_id):
        self.elector_residence_id = elector_residence_id

    def getElector_change_log(self):
        return [self.elector_change_log_id, self.elector_id, self.elector_doc_id, self.elector_residence_id,
                self.elector_zags_info_id, self.sys_elector_id, self.change_type_id, self.change_number,
                self.change_date, self.is_actual, self.start_date2, self.create_user_id, self.input_source, self.kca,
                self.change_basis_id, self.is_death, self.is_deleted, self.import_log_id, self.is_approved,
                self.start_date2, self.update_user_id, self.is_departured_in_military, self.is_departured_from_addr,
                self.is_departured_in_prison, 'избиратель']
