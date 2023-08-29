# Проект парсинга pep
Cобирает информацию об обновлениях версий Python и PEP-документациях.

## Возможности:
- Сброр ссылок на статьи о нововведениях в Python
- Скачивание архива с актуальной документацией
- Подсчет документов PEP, находящихся в разных статусах
- Получение данных в формате csv.
  
## Стек технологий:
[![Python](https://img.shields.io/badge/-Python-464646?style=flat&logo=Python&logoColor=ffffff&color=043A6B)](https://www.python.org/)
[![BeautifulSoup4](https://img.shields.io/badge/-BeautifulSoup4-464646?style=flat&logo=BeautifulSoup4&logoColor=ffffff&color=043A6B)](https://www.crummy.com/software/BeautifulSoup/)

 
 ## Запуск проекта
- Клонировать репозиторий и перейти в директорию проекта
```
git clone https://github.com/jullitka/bs4_parser_pep.git
cd bs4_parser_pep
```
- Cоздать и активировать виртуальное окружение:

```
python -m venv env
```
Для Linux
```
source venv/bin/activate
```
Для Windows
```
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
