# Парсим онлайн-библиотеку
В данном великолепном проекте Вы сможете получить всю информацию с онлайн-библиотеки [tululu.org](tululu.org). Вы сможете скачать книги, получить их название, автора и много всего интересного.

## Как установить
Для запуска сайта у вас уже должен быть установлен Python 3.

- Скачайте код
- Установите зависимости командой 
``` python
pip install -r requirements.txt
```
- Запустите скрипт командой 
``` python
python main.py
```

## Необязательные аргументы
В данном проекте присутвуют необязательные аргументы, такие как `--start_id` и `--end_id`:

1. `--start_id` или же `-s` - это число, которое обозначает айди книги, с которой нужно начинать скачивание, по молчанию стоит: 1
2. `--end_id` или же `-e` - это число, которое обозначает айди книги, которой нужно закончить скачивание, по умолчанию стоит: 10

## Пример запуска
Если Вы хотите скачать книги от 1 до 10:
``` python
python main.py
```

Если Вы хотите скачать книги от 20 до 30:
```python 
python main.py -s 20 -e 30
```

И так далее...

## Цели проекта
Код написан в учебных целях — это урок в курсе по Python и веб-разработке на сайте [Devman](https://dvmn.org).
