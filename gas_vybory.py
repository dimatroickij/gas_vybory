from contextlib import closing

import psycopg2
from mimesis import Person
from psycopg2.extras import DictCursor


def generateUIP():
    pass


def DB():
    with closing(psycopg2.connect(dbname='gas20dev', user='voshod',
                                  password='voshod', host='172.20.101.55')) as conn:
        with conn.cursor() as cursor:
            pass

            # Создание записи в таблице person.elector (таблица с УИП)
            sys_elector_id = 123456789

            cursor.execute("""
                insert into person.elector (last_name, first_name, middle_name, birth_day, birth_day_string, gender_id,
                capacity_id, country_id, start_date, input_source_id, sys_elector_id, address_id) values
                (%(last_name)s, %(first_name)s, %(middle_name)s, %(birth_day)s, %(birth_day_string)s, %(gender_id)s,
                %(capacity_id)s, 643, %(start_date)s, 1, %(sys_elector_id)s, 1)
                """, {'last_name': 'last_name', 'first_name': 'first_name', 'middle_name': 'middle_name',
                      'birth_day': 'birth_day', 'birth_day_string': 'birth_day_string', 'gender_id': 1,
                      'capacity_id': 1, 'start_date': 'start_date', 'sys_elector_id': sys_elector_id})

            # создание записи в таблице person.elector_king (статус УИП)
            cursor.execute("""
                insert into person.elector_kind (sys_elector_id, create_date, elector_kinds_json) values 
                (%(sys_elector_id)s, %(create_date)s, '[{"id": 1}]')""", {'sys_elector_id': sys_elector_id,
                                                                          'create_date': 'create_date'})

            # Создание записи в таблице person.elector_doc (данные документа УИПа)
            cursor.execute("""
                insert into person.elector_doc (subject_id, elector_doc_code_id, elect_doc_series, elect_doc_number, 
                input_source_id, start_date, elect_doc_issue_date, elector_doc_type_id, sys_elector_id) values 
                (%(subject_id)s, 10, %(elect_doc_series)s, %(elect_doc_number)s, 1, %(start_date)s, 
                %(elect_doc_issue_date)s, 9, %(sys_elector_id)s)""",
                           {'subject_id': 'subject_id', 'elect_doc_series': 'elect_doc_series',
                            'elect_doc_number': 'elect_doc_number', 'start_date': 'start_date',
                            'elect_doc_issue_date': 'elect_doc_issue_date', 'sys_elector_id': sys_elector_id})

            # Создание записи в таблице person.elector_residence (данные о месте жительства)
            cursor.execute("""
                insert into person.elector_residence (input_source, elector_residence_kind_id, start_date, 
                sys_elector_id, residence_address_id) values (1, 1, %(start_date)s, %(sys_elector_id)s,
                %(residence_address_id)s)""", {'start_date': 'start_date', 'sys_elector_id': sys_elector_id,
                                               'residence_address_id': 'residence_address_id'})

            # Создание записи в таблице person.elector_change_log (история изменений УИПа.
            #                                                      Будут создаваться записи Рождение)
            cursor.execute("""
                insert into person.elector_change_log (elector_zags_info_id, change_type_id, change_number, change_date, input_source_id, change_basis_id, import_log_id, update_user_id, elector_id, elector_doc_id, elector_residence_id, elector_zags_info_idn, sys_elector_id, kind_names)""")
            # cursor.execute("""SELECT * FROM person.elector limit %(count)s""", {'count': 2})
            # for row in cursor:
            #     print(row)