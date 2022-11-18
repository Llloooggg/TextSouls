# TextSouls

### Бэкенд
Все действия производить из папки backend!

###### Получение карты эндпоинтов для Postman
```
flask2postman textsouls.app --name "TextSouls" --folders > text_souls_postman.json
```

###### Создание/подготовка БД
```
scripts/updatedb.sh
```
###### Запуск
```
scripts/runserver.sh
```

### Запуск Telegram
Из папки Telegram:
```
python textsouls/main.py
```