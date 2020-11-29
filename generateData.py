import csv
import json

# Для создания массива с ID адреса необходимо вытащить csv файл таблицы address
import uuid
import bcrypt
import psycopg2


def genResidenceAddressFile():
    keys = []
    with open('address.csv', 'r', encoding='UTF-8') as address_file:
        csv_people = csv.reader(address_file, delimiter='|')
        for row in csv_people:
            # колонка address_level_id, 17 - квартира
            if row[26] == '17':
                # колонка address_id
                keys.append(row[22])
    with open('residence_id.csv', 'w', encoding='UTF-8') as residence_id_file:
        csv_residence_file = csv.writer(residence_id_file, delimiter='|')
        csv_residence_file.writerow(keys)


def generateSys_userAndIK(startID=1000000, plotsId=100000):
    IK = []
    sys_user = []
    plots_territories = []
    hashedPassword = bcrypt.hashpw('1111'.encode(), bcrypt.gensalt())  # хеш от пароля для загрузки в БД

    # Добавление ИУ с заданными параметрами, целевая таблица: nsi.subject
    def addIK(subject_id, subject_name, subject_level_id, subject_rf_id, is_protected, kca, subject_full_name, lvl,
              subject_global_parent_id):
        is_actual = True
        begin_date = end_date = None
        subject_type_id = 1  # 1 - избирательные комиссии
        municipal_type = election_level = None
        is_unchecked = False
        create_date = update_date = '2020-04-03 00:00:00'
        create_user_id = update_user_id = '28d1bdea-5e04-11ea-bc55-0242ac130003'
        left_count = right_count = None
        subject_code = None
        subject_global_id = subject_id
        election_company_name_id = None
        IK.append([subject_id, is_actual, begin_date, end_date, subject_name, subject_type_id, subject_level_id,
                   municipal_type, election_level, subject_rf_id, is_unchecked, is_protected, create_date,
                   create_user_id, update_date, update_user_id, kca, subject_full_name, lvl, left_count, right_count,
                   subject_code, subject_global_id, subject_global_parent_id, election_company_name_id])

    # Добавление учетных записей к ИУ с заданными параметрами, целевая таблица: auth.sys_user
    def addUser(subject_global_id, ikCode, ikName, kca, subject_rf_id, user_role_id, address_id):
        for i in range(1, 5):
            sys_user_id = uuid.uuid4()
            sys_user_email = ikCode + str(i)
            family_name = ikName + ", " + str(i) + ' УЗ'
            first_name = ikName + " " + str(i)
            patronymic = ikName + " " + str(i)
            sys_user_password = hashedPassword.decode()
            create_date = '2020-04-03 00:00:00'
            update_date = create_user_id = update_user_id = None
            is_deleted = False
            usesysid = None
            sys_user.append([sys_user_id, sys_user_email, family_name, first_name, patronymic, kca, subject_global_id,
                             subject_rf_id, user_role_id, sys_user_password, create_date, update_date, create_user_id,
                             update_user_id, is_deleted, address_id, usesysid])

    # Добавление ТИКов и УИКов в базу для модуля ФСИ, целевая таблица: nsi.plots_territories_new_copy
    def addPlotsTerritory(plots_territories_id, name_ik, vid_ik, district_num, subject_rf_code, subject_global_id, kca,
                          subject_id):
        district_type = 1
        parent_ksa = vcpr_tech = None
        numbers_res_id = slicing_res_id = dateout = notes = None
        is_actual = True
        create_date = '2020-09-06 18:38:40'
        create_user_id = update_date = update_user_id = None
        elector_district_category = 100100025537261  # городской участок, id из таблицы elector_district_category
        fed_territory_id = address_id = begin_date = end_date = district_phone = None

        plots_territories.append([plots_territories_id, name_ik, vid_ik, district_num, district_type, subject_rf_code,
                                  parent_ksa, vcpr_tech, numbers_res_id, slicing_res_id, dateout, notes, is_actual,
                                  create_date, create_user_id, update_date, update_user_id, elector_district_category,
                                  subject_global_id, fed_territory_id, kca, address_id, begin_date, end_date,
                                  district_phone, subject_id])

    with open('data/subject_rf.csv', 'r', encoding='UTF-8') as subject_rf_file:
        csv_subject_rf = csv.reader(subject_rf_file, delimiter='|')
        subject_rf_list = []
        exceptRf = ['Агинский Бурятский автономный округ', 'Город Байконур (Республика Казахстан)',
                    'Коми-Пермяцкий автономный округ', 'Камчатская область', 'Корякский автономный округ',
                    'Российская Федерация', 'Пермская область',
                    'Таймырский (Долгано-Ненецкий) автономный округ', 'Территория за пределами РФ',
                    'Усть-Ордынский Бурятский автономный округ', 'Читинская область', 'Эвенкийский автономный округ']
        for subject in csv_subject_rf:
            if subject[2] not in exceptRf:
                subject_rf_list.append(
                    {'subject_rf_id': subject[0], 'subject_rf_name': subject[2], 'genetive_s_name': subject[3],
                     'subject_rf_code': subject[4]})

        # Добавление ЦИКа (41 - код ЦИК из БД)
        addIK(startID, 'ЦИК (00С000) тест', 41, None, True, '00C000', 'ЦИК: Избирательные комиссии (ИК) 00C000', 1,
              None)

        # Добавление учетных записей, привязанных к ЦИКу
        addUser(startID, 'cik', 'ЦИК', '00C000', 0, 1, 1)

        # Добавление ИКСРФ (42 - код ИКСРФ из БД)
        i = 1
        for subject in subject_rf_list:
            nameTIK = 'Избирательная комиссия ' + subject['genetive_s_name']
            kca = subject['subject_rf_code'] + 'T000'
            addIK(startID + i, nameTIK, 42, subject['subject_rf_id'], False, kca, nameTIK, 2, startID)

            # Добавление учетных записей, привязанных к ТИКу
            addUser(startID + i, 'tik' + subject['subject_rf_code'] + '_', 'ТИК ' + subject['subject_rf_code'] +
                    ' регион', kca, subject['subject_rf_id'], 3, 1)
            # addPlotsTerritory(id, name_ik, vid_ik, district_num, subject_rf_code, subject_global_id, kca):
            addPlotsTerritory(plotsId + i, nameTIK, 42, 1, subject['subject_rf_code'], startID + i, kca, startID + i)
            i += 1

        # Создание ТИК, подчиненных областным ТИК
        j = 1
        for mainTIK in subject_rf_list:
            for dependTikID in range(1, 32):
                nameTIK = 'ТИК №' + str(dependTikID) + ' ' + mainTIK['genetive_s_name']
                kca = mainTIK['subject_rf_code'] + 'T0%s' % (str(0) * (len(str(dependTikID)) % 2) + str(dependTikID))
                addIK(startID + i, nameTIK, 45, mainTIK['subject_rf_id'], False, kca, nameTIK, 3, startID + j)

                # Добавление учетных записей, привязанных к ТИКу
                addUser(startID + i, 'tik' + subject['subject_rf_code'] + '_' + str(dependTikID) + '_',
                        'ТИК №' + str(dependTikID) + ' ' + subject['subject_rf_code'] +
                        ' регион', kca, subject['subject_rf_id'], 3, 1)
                addPlotsTerritory(plotsId + i, nameTIK, 45, 1, subject['subject_rf_code'], startID + i, kca,
                                  startID + i)
                i += 1
            j += 1

        num = 86
        code = 1
        # Создание УИКов, подчиненных обычным ТИКам, 46 - код УИКа в БД
        for dependTik in IK[86:2721]:
            if (num - 86) % 31 == 0:
                code = 1
            for uikID in range(1, 20):
                nameUIK = 'Участковая избирательная комиссия №%i' % code
                addIK(startID + i, nameUIK, 46, dependTik[9], False, dependTik[16], nameUIK, 4, dependTik[0])
                addPlotsTerritory(plotsId + i, nameUIK, 46, uikID, dependTik[16][0:2], startID + i,
                                  dependTik[16], startID + i)
                i += 1
                code += 1
            num += 1

        with open('D:\\genFileGAS_Vybory\IK.csv', "w", newline='',
                  encoding='UTF-8') as ik_file:
            csv_ik = csv.writer(ik_file, delimiter='|')
            for ik in IK:
                csv_ik.writerow(ik)

        with open('D:\\genFileGAS_Vybory\sys_user.csv', "w", newline='',
                  encoding='UTF-8') as sys_user_file:
            csv_sys_user = csv.writer(sys_user_file, delimiter='|')
            for user in sys_user:
                csv_sys_user.writerow(user)

        with open('D:\\genFileGAS_Vybory\plots_territories.csv', "w", newline='',
                  encoding='UTF-8') as plots_territories_file:
            csv_plots_territories = csv.writer(plots_territories_file, delimiter='|')
            for plot in plots_territories:
                csv_plots_territories.writerow(plot)


generateSys_userAndIK()
