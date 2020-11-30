Порядок загрузки и генерации данных:

1) В таблицу nsi.subject импортировать файл /data/subject_passport.csv с разделителем |
2) Экспортировать таблицу admin.address через pgAdmin с разделителем |, назвать файл address.csv.
    Нужные колонки должны идти в следующей последовательности:
    'address_name', 'is_atom', 'is_basic', 'is_actual', 'is_unchecked', 'is_protected', 'subject_rf_id',
    'address_id', 'address_parent_id', 'address_level_child_id', 'address_level_id', 'address_parent_id_array'
4) Экспортировать таблицу nsi.subject_rf через pgAdmin с разделителем |, назвать файл /data/subject_rf.csv
5) Запустить скрипт generateData.getSubjectRf(путь до файла address.csv)
5) Запустить скрипт generateData.generateSys_userAndIK()
6) В таблицу nsi.subject импортировать файл IK.csv с разделителем |
7) В таблицу auth.sys_user импортировать файл sys_user.csv с разделителем |
8) В таблицу nsi.plots_territories имортировать файл plots_territories.csv с разделителем |


!!! Запуск скрипта по генерации данных УИПа !!!
9) Запустить скрипт generateData.genResidenceAddressFile()
10) В таблицу person.elector импортировать файл elector.csv с разделителем |
11) В файле elector_king.csv заменить |"[{""id"": 1}]"| на |"[{'"id'": 1}]"|
12) В таблицу person.elector_king импортировать файл elector_king.csv с разделителем |
13) В таблицу person.elector_doc импортировать файл elector_doc.csv с разделителем |
14) В таблицу person.elector_residence импортировать файл elector_residence.csv с разделителем |
15) В таблицу person.elector_change_log импортировать файл elector_change_log.csv с разделителем |