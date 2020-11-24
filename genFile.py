import csv
import json
from datetime import datetime
from multiprocessing import Process
from genPeople import UIP


def saveFile(count, number):
    print('start %s' % number)
    peopleFile = None
    with open("person.json", "r", encoding='UTF-8') as read_file:
        peopleFile = json.load(read_file)

    residenceFile = None
    with open("residence_id.csv", "r", encoding='UTF-8') as read_file:
        residence = csv.reader(read_file, delimiter='|')
        residenceFile = list(residence)[0]

    # subjectFile = None
    # with open("subject_id.json", "r", encoding='UTF-8') as read_file:
    #     subjectFile = json.load(read_file)

    for i in range(1, count + 1):
        with open('D:\\genFileGAS_Vybory\elector%s.csv' % number, "a", newline='', encoding='UTF-8') as people_file:
            with open('D:\\genFileGAS_Vybory\elector_kind%s.csv' % number, "a", newline='',
                      encoding='UTF-8') as kind_file:
                with open('D:\\genFileGAS_Vybory\elector_doc%s.csv' % number, "a", newline='',
                          encoding='UTF-8') as doc_file:
                    with open('D:\\genFileGAS_Vybory\elector_residence%s.csv' % number, "a", newline='',
                              encoding='UTF-8') as residence_file:
                        with open('D:\\genFileGAS_Vybory\elector_change_log%s.csv' % number, "a", newline='',
                                  encoding='UTF-8') as change_log_file:
                            csv_people = csv.writer(people_file, delimiter='|')
                            csv_kind = csv.writer(kind_file, delimiter='|')
                            csv_doc = csv.writer(doc_file, delimiter='|')
                            csv_residence = csv.writer(residence_file, delimiter='|')
                            csv_change_log = csv.writer(change_log_file, delimiter='|')

                            people = UIP(ageMin=18, ageMax=80, capacity=1, sys_elector_id=77786132 + i,
                                         elector_id=22892527 + i, elector_change_log_id=7662 + i,
                                         elector_kind_id=6450 + i, elector_doc_id=62000 + i,
                                         elector_residence_id=222723 + i, peopleFile=peopleFile,
                                         residenceFile=residenceFile)

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
    count = 10
    countProcess = 1

    startWork = datetime.now().timestamp()
    procs = []
    for i in range(1, countProcess + 1):
        proc = Process(target=saveFile, args=(count, '%i' % i))
        procs.append(proc)
        proc.start()

    for proc in procs:
        proc.join()

    total = count * countProcess / (datetime.now().timestamp() - startWork)
    avgHour = 150_000_000 / total / 60 / 60
    avgDay = avgHour / 24
    print('Средняя скорость создания записей: %f в секунду' % total)
    print('Среднее время создания 150_000_000 записей: %f часов или %f дней' % (avgHour, avgDay))
