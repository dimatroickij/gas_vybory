Порядок загрузки и генерации данных:
1) В таблицу nsi.subject экспортировать файл subject_passport.csv с разделителем |
2) Импортировать таблицу admin.address через pgAdmin с разделителем |, назвать файл address.csv
3) Запустить скрипт generateData.genResidenceAddressFile()
4) Импортировать таблицу nsi.subject_rf через pgAdmin с разделителем |, назвать файл subject_rf.csv
5) Запустить скрипт


В файле elector_king.csv заменить |"[{""id"": 1}]"| на |"[{'"id'": 1}]"|