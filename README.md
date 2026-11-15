# Books Scraper

## Цель проекта
Сбор данных о книгах с сайта Books to Scrape

## Инструкция по запуску
1. Клонируйте репозиторий: git clone https://github.com/yakov19864/HW_03_python_parser
2. Создайте и активируйте виртуальное окружение:
   python3 -m venv venv
   source venv/bin/activate
3. Установите зависимости: pip install -r requirements.txt
4. Запустите парсер: python scraper.py
5. Для запуска тестов: PYTHONPATH=. pytest tests/test_scraper.py -v

## Используемые библиотеки
- requests: отправка HTTP-запросов
- beautifulsoup4: парсинг HTML-разметки
- pytest: написание и запуск автотестов
- schedule: автоматизация запуска по расписанию
