import csv
from datetime import datetime

from genPeople import UIP

count = 10
date_start = datetime.now().timestamp()
with open('D:\\elector.csv', "w", newline='', encoding='UTF-8') as people_file:
    with open('D:\\elector_kind.csv', "w", newline='', encoding='UTF-8') as kind_file:
        with open('D:\\elector_doc.csv', "w", newline='', encoding='UTF-8') as doc_file:
            with open('D:\\elector_residence.csv', "w", newline='', encoding='UTF-8') as residence_file:
                with open('D:\\elector_change_log.csv', "w", newline='', encoding='UTF-8') as change_log_file:
                    csv_people = csv.writer(people_file, delimiter='|')
                    csv_kind = csv.writer(kind_file, delimiter='|')
                    csv_doc = csv.writer(doc_file, delimiter='|')
                    csv_residence = csv.writer(residence_file, delimiter='|')
                    csv_change_log = csv.writer(change_log_file, delimiter='|')

                    for i in range(1, count + 1):
                        people = UIP(gender=1, ageMin=18, ageMax=20, capacity=1, sys_elector_id=77786132 + i,
                                     elector_id=22892527 + i, elector_change_log_id = 7662 + i,
                                     elector_kind_id = 6450 + i, elector_doc_id=62000 + i,
                                     elector_residence_id=222723 + i, residence_address_id=144082079413834240000345981,
                                     address_id=1)
                        csv_people.writerow(people.getElector())
                        #[self.elector_kind_id, self.sys_elector_id, self.create_date, self.elector_kinds_json,
                #self.has_external_vision]
                        # kind_file.write(str(people.elector_kind_id) + '|' + str(people.sys_elector_id) + '|' +
                        #                 people.create_date + '|' + people.elector_kinds_json + '|' +
                        #                 str(people.has_external_vision) + '\n')
                        csv_kind.writerow(people.getElector_kind())
                        csv_doc.writerow(people.getElector_doc())
                        csv_residence.writerow(people.getElector_residence())
                        csv_change_log.writerow(people.getElector_change_log())

print((datetime.now().timestamp() - date_start))
