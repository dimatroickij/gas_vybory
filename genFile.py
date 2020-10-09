import csv
import json
from datetime import datetime
from multiprocessing import Process
from threading import Thread

from genPeople import UIP


def saveFile(count, number):
    print('start %s' % number)
    for i in range(1, count + 1):
        if i % 1000 == 0:
            print(str(i) + ' / 1_000_000')
        with open('F:\\genFileGAS_Vybory\elector%i.csv' % number, "a", newline='', encoding='UTF-8') as people_file:
            with open('F:\\genFileGAS_Vybory\elector_kind%i.csv' % number, "a", newline='',
                      encoding='UTF-8') as kind_file:
                with open('F:\\genFileGAS_Vybory\elector_doc%i.csv' % number, "a", newline='',
                          encoding='UTF-8') as doc_file:
                    with open('F:\\genFileGAS_Vybory\elector_residence%i.csv' % number, "a", newline='',
                              encoding='UTF-8') as residence_file:
                        with open('F:\\genFileGAS_Vybory\elector_change_log%i.csv' % number, "a", newline='',
                                  encoding='UTF-8') as change_log_file:
                            csv_people = csv.writer(people_file, delimiter='|')
                            csv_kind = csv.writer(kind_file, delimiter='|')
                            csv_doc = csv.writer(doc_file, delimiter='|')
                            csv_residence = csv.writer(residence_file, delimiter='|')
                            csv_change_log = csv.writer(change_log_file, delimiter='|')

                            people = UIP(gender=1, ageMin=0, ageMax=13, capacity=1,
                                         sys_elector_id=1_000_000_000 + i + count * (number - 1),
                                         elector_id=4_000_000_000 + i + count * (number - 1),
                                         elector_change_log_id=1_000_000 + i + count * (number - 1),
                                         elector_kind_id=100_000 + i + count * (number - 1),
                                         elector_doc_id=100_000 + i + count * (number - 1),
                                         elector_residence_id=100_000 + i + count * (number - 1))

                            # print(people.getElector())
                            # print(people.getElector_kind())
                            # print(people.getElector_doc())
                            # print(people.getElector_residence())
                            # print(people.getElector_change_log())

                            csv_people.writerow(people.getElector())
                            csv_kind.writerow(people.getElector_kind())
                            csv_doc.writerow(people.getElector_doc())
                            csv_residence.writerow(people.getElector_residence())
                            csv_change_log.writerow(people.getElector_change_log())
    print('end process %s' % number)



if __name__ == '__main__':
    count = 1_000_000
    countProcess = 2

    startWork = datetime.now().timestamp()
    procs = []
    for i in range(1, countProcess + 1):
        proc = Process(target=saveFile, args=(count, i))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    total = count * countProcess  / (datetime.now().timestamp() - startWork)
    avgHour = 150_000_000 / total / 60/ 60
    avgDay = avgHour / 24
    print('Средняя скорость создания записей: %f в секунду' % total)
    print('Среднее время создания 150_000_000 записей: %f часов или %f дней' % (avgHour, avgDay))
    print(datetime.now())