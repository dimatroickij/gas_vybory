import csv
import gc
import json
import random

from genPeople import UIP
#
# # with open('person.csv', "w", newline='', encoding='UTF-8') as csv_file:
# #     writer = csv.writer(csv_file, delimiter='|')
# #
# #     for i in range(0, 200):
# #         people = UIP(gender=1, ageMin=18, ageMax=20, capacity=1, sys_elector_id=7778613 + 1, elector_id=2289257 + i,
# #                      elector_doc_id=6000 + i, elector_residence_id=14723 + i,
# #                      residence_address_id=144082079413834240000345981)
# #         writer.writerow(people.getElector_file())
# #         del people
# #         print('%i / 1000' % i)
for i in range(0, 2000):
    people = UIP(gender=1, ageMin=18, ageMax=20, capacity=1, sys_elector_id=7778613 + 1, elector_id=2289257 + i,
                 elector_doc_id=6000 + i, elector_residence_id=14723 + i,
                 residence_address_id=144082079413834240000345981)

    print('%i / 1000' % i)
