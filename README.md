# TextSouls


### Бэкенд
Все действия производить из папки backend!

###### Получение карты эндпоинтов для Postman
```
flask2postman textsouls.app --name "TextSouls" --folders > text_souls_postman.json
```

###### Создание/обновление БД
```
scripts/updatedb.sh
```

###### Вставка начальных данных
```
python ./scripts/seed_inserter.py
```

###### Запуск
```
scripts/runserver.sh
```


### Запуск Telegram
Из папки telegram:
```
python textsouls/main.py
```