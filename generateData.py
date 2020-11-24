import csv
import json


# Для создания массива с ID адреса необходимо вытащить csv файл таблицы address
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


def genIKFile():
    IK = []
    with open('data/subject_rf.csv', 'r', encoding='UTF-8') as subject_rf_file:
        csv_subject_rf = csv.reader(subject_rf_file, delimiter='|')
        subject_rf_list = []
        exceptRf = ['Агинский Бурятский автономный округ', 'Город Байконур (Республика Казахстан)',
                    'Коми-Пермяцкий автономный округ', 'Камчатская область', 'Корякский автономный округ',
                    'Российская Федерация', 'Пермская область',
                    'Таймырский (Долгано-Ненецкий) автономный округ', 'Территория за пределами РФ',
                    'Усть-Ордынский Бурятский автономный округ', 'Читинская область', 'Эвенкийский автономный округ']
        for row in csv_subject_rf:
            if row[2] not in exceptRf:
                subject_rf_list.append({'subject_rf_id': row[0], 'subject_rf_name': row[2], 'genetive_s_name': row[3],
                                        'subject_rf_code': row[4]})
        # структура таблицы subject: subject_id|is_actual|begin_date|end_date|subject_name|subject_type_id|
        # subject_level_id|municipal_type|election_level|subject_rf_id|is_unchecked|is_protected|create_date|
        # create_user_id|update_date|update_user_id|kca|subject_full_name|lvl|left_count|right_count|subject_code|
        # subject_global_id|subject_global_parent_id|election_company_name_id

        # 1 - избирательные комиссии
        # Добавление ЦИКа (41 - код ЦИК из БД)
        startID = 1000000
        IK.append([startID, True, None, None, 'ЦИК (00С00) тест', 1, 41, None, None, None, False, True,
                   '2020-04-03 00:00:00', '28d1bdea-5e04-11ea-bc55-0242ac130003', '2020-04-03 00:00:00',
                   '28d1bdea-5e04-11ea-bc55-0242ac130003', '00C00', 'ЦИК: Избирательные комиссии (ИК) 00C000',
                   1, None, None, None, startID, None, None])

        # Добавление областных ТИКов (45 - код ТИК из БД)
        i = 1
        for subject in subject_rf_list:
            IK.append([startID + i, True, None, None, 'Избирательная комиссия ' + subject['genetive_s_name'],
                       1, 45, None, None, subject['subject_rf_id'], False, False, '2020-04-03 00:00:00',
                       '28d1bdea-5e04-11ea-bc55-0242ac130003', '2020-04-03 00:00:00',
                       '28d1bdea-5e04-11ea-bc55-0242ac130003', subject['subject_rf_code'] + 'T000',
                       'Избирательная комиссия ' + subject['genetive_s_name'], 2, None, None, None, startID + i,
                       startID, None])
            i += 1
        # Создание ТИК, подчиненных областным ТИК
        j = 1
        for mainTIK in subject_rf_list:
            for dependTikID in range(1, 32):
                IK.append([startID + i, True, None, None, 'ТИК %i %s' % (dependTikID, mainTIK['genetive_s_name']),
                           1, 45, None, None, mainTIK['subject_rf_id'], False, False, '2020-04-03 00:00:00',
                           '28d1bdea-5e04-11ea-bc55-0242ac130003', '2020-04-03 00:00:00',
                           '28d1bdea-5e04-11ea-bc55-0242ac130003', mainTIK['subject_rf_code'] + 'T0%i' % dependTikID,
                           'ТИК %i %s' % (dependTikID, mainTIK['genetive_s_name']), 3, None, None, None, startID + i,
                           startID + j, None])
                i += 1
            j += 1

        # Создание УИКов, подчиненных обычным ТИКам, 46 - код УИКа в БД
        for dependTik in IK[86:2721]:
            for uikID in range(1, 20):
                IK.append([startID + i, True, None, None, 'Участковая избирательная комиссия №%i' % uikID,
                           1, 46, None, None, dependTik[9], False, False, '2020-04-03 00:00:00',
                           '28d1bdea-5e04-11ea-bc55-0242ac130003', '2020-04-03 00:00:00',
                           '28d1bdea-5e04-11ea-bc55-0242ac130003', dependTik[16],
                           'Участковая избирательная комиссия №%i' % uikID, 4, None, None, None, startID + i,
                           dependTik[23], None])
                i += 1

        with open('D:\\genFileGAS_Vybory\IK.csv', "a", newline='',
                  encoding='UTF-8') as ik_file:
            csv_ik = csv.writer(ik_file, delimiter='|')
            for ik in IK:
                csv_ik.writerow(ik)
genIKFile()
