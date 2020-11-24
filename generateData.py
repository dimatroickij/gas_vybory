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


# def genSubjectIdFile():
#     keys = {0: [], 1: []}
#     with open('subject.csv', 'r', encoding='UTF-8') as subject_file:
#         csv_subject = csv.reader(subject_file, delimiter='|')
#         for row in csv_subject:
#             if int(row[7]) in [2, 9, 100]:
#                 keys[0].append(row[1])
#             elif int(row[7]) == 3:
#                 keys[1].append(row[1])
#     with open('subject_id.json', 'w', encoding='UTF-8') as subject_id_file:
#         json.dump(keys, subject_id_file)
