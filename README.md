# Проект парсинга pep
Парсер собирает информацию об обновлениях версий Python и PEP-документациях.

## Возможности:
- Сброр ссылок на статьи о нововведениях в Python;
- Скачивание архива с актуальной документацией;
- Подсчет документов PEP, находящихся в разных статусах.
- Получение данных в формате csv.
 
 ## Запуск проекта
- Клонирование репозитория
```
git clone https://github.com/jullitka/bs4_parser_pep.git
```

- Cоздать и активировать виртуальное окружение:
```
python3 -m venv venv
source venv/Scripts/activate
```
- Установить зависимости из файла requirements.txt:
```
python3 -m pip install --upgrade pip
pip install -r requirements.txt
```

## Аргументы командной строки 
Вывести список аргументов:
```
python main.py -h
```
```
usage: main.py [-h] [-c] [-o {pretty,file}]
               {whats-new,latest-versions,download,pep}

Парсер документации Python

positional arguments:
  {whats-new,latest-versions,download,pep}
                        Режимы работы парсера

optional arguments:
  -h, --help            show this help message and exit
  -c, --clear-cache     Очистка кеша
  -o {pretty,file}, --output {pretty,file}
                        Дополнительные способы вывода данных
```
