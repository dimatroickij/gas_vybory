from contextlib import closing

import psycopg2
from mimesis import Person
from psycopg2.extras import DictCursor

from genPeople import UIP


class workDB:
    def __init__(self):
        pass

    def set_people(self, people):
        self.people = people

    def openDB(self):
        self.conn = psycopg2.connect(dbname='gas20dev', user='voshod', password='voshod', host='')
        self.cursor = self.conn.cursor()

    # Создание записи в таблице person.elector (таблица с УИП)
    def createElector(self):
        elector = self.people.getElector()
        self.cursor.execute("""insert into person.elector (last_name, first_name, middle_name, birth_day, 
                                birth_day_string, gender_id, capacity_id, country_id, start_date, input_source_id, 
                                sys_elector_id, address_id) values (%(last_name)s, %(first_name)s, %(middle_name)s, 
                                %(birth_day)s, %(birth_day_string)s, %(gender_id)s, %(capacity_id)s, %(country_id)s, 
                                %(start_date)s, %(input_source)s, %(sys_elector_id)s, %(address_id)s)""",
                            {'last_name': elector[2], 'first_name': elector[3], 'middle_name': elector[4],
                             'birth_day': elector[5], 'birth_day_string': elector[6], 'gender_id': elector[8],
                             'capacity_id': elector[9], 'country_id': elector[11], 'start_date': elector[14],
                             'input_source': elector[16], 'sys_elector_id': elector[1], 'address_id': elector[10]})
        self.conn.commit()

    def setElector_id(self):
        self.cursor.execute('select elector_id from person.elector where sys_elector_id = %s'
                            % self.people.sys_elector_id)
        for row in self.cursor:
            self.people.setElector_id(row[0])

    def createElectorKind(self):
        king = self.people.getElector_kind()
        self.cursor.execute("""insert into person.elector_kind (sys_elector_id, create_date, elector_kinds_json) values 
                            (%(sys_elector_id)s, %(create_date)s, %(elector_kinds_json)s)""",
                            {'sys_elector_id': king[1], 'create_date': king[2], 'elector_kinds_json': king[3]})
        self.conn.commit()

    # Создание записи в таблице person.elector_doc (данные документа УИПа)
    def createElector_doc(self):
        doc = self.people.getElector_doc()
        self.cursor.execute("""insert into person.elector_doc (subject_global_id, elector_doc_code_id, elect_doc_series, 
                            elect_doc_number, input_source_id, start_date, elect_doc_issue_date, elector_doc_type_id, 
                            sys_elector_id) values (%(subject_id)s, %(elector_doc_code_id)s, %(elect_doc_series)s, 
                            %(elect_doc_number)s, %(input_source)s, %(start_date)s, %(elect_doc_issue_date)s,
                            %(elector_doc_type_id)s, %(sys_elector_id)s)""",
                            {'subject_id': doc[2], 'elector_doc_code_id': doc[3], 'elect_doc_series': doc[4],
                             'elect_doc_number': doc[5], 'input_source': doc[6], 'start_date': doc[7],
                             'elect_doc_issue_date': doc[11], 'elector_doc_type_id': doc[12], 'sys_elector_id': doc[1]})
        self.conn.commit()

    def setElector_doc_id(self):
        self.cursor.execute('select elector_doc_id from person.elector_doc '
                            'where sys_elector_id = %s' % self.people.sys_elector_id)
        for row in self.cursor:
            self.people.setElector_doc_id(row[0])
        #print(self.people.elector_doc_id)

    # Создание записи в таблице person.elector_residence (данные о месте жительства)
    def createElector_recidence(self):
        residence = self.people.getElector_residence()
        self.cursor.execute("""insert into person.elector_residence (input_source, elector_residence_kind_id, 
                            start_date, sys_elector_id, residence_address_id) values (%(input_source)s, 
                            %(elector_residence_kind_id)s, %(start_date)s, %(sys_elector_id)s, 
                            %(residence_address_id)s)""", {'input_source': residence[7],
                                                           'elector_residence_kind_id': residence[8],
                                                           'start_date': residence[9], 'sys_elector_id': residence[1],
                                                           'residence_address_id': residence[2]})
        self.conn.commit()

    def setElector_residence_id(self):
        self.cursor.execute('select elector_residence_id from person.elector_residence '
                            'where sys_elector_id = %s' % self.people.sys_elector_id)
        for row in self.cursor:
            self.people.setElector_residence_id(row[0])
        #print(self.people.elector_residence_id)

    # Создание записи в таблице person.elector_change_log (история изменений УИПа)
    def createElector_change_log(self):
        change_log = self.people.getElector_change_log()
        self.cursor.execute("""insert into person.elector_change_log (change_type_id, 
                                change_number, change_date, input_source_id, change_basis_id, 
                                elector_id, elector_doc_id, elector_residence_id, kca, 
                                sys_elector_id) values (%(change_type_id)s, %(change_number)s, %(change_date)s,
                                %(input_source_id)s, %(change_basis_id)s, %(elector_id)s, %(elector_doc_id)s,
                                %(elector_residence_id)s, %(kca)s, %(sys_elector_id)s)""",
                            {'change_type_id': change_log[6], 'change_number': change_log[7],
                             'change_date': change_log[8], 'input_source_id': change_log[12],
                             'change_basis_id': change_log[14], 'elector_id': change_log[1],
                             'elector_doc_id': change_log[2], 'elector_residence_id': change_log[3],
                             'kca': change_log[13], 'sys_elector_id': change_log[5]})
        self.conn.commit()

db = workDB()
db.openDB()
i = 10
people = UIP(gender=1, ageMin=10, ageMax=13, capacity=1, sys_elector_id=77786132 + i, elector_id=22892527 + i,
             elector_change_log_id=7662 + i, elector_kind_id=6450 + i, elector_doc_id=62000 + i,
             elector_residence_id=222723 + i)
db.set_people(people)
db.createElector()
db.setElector_id()
db.createElectorKind()
db.createElector_doc()
db.setElector_doc_id()
db.createElector_recidence()
db.setElector_residence_id()
db.createElector_change_log()
