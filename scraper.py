
import json
import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup


def get_book_data(book_url: str) -> dict:
    """
    Получаю инф-цию с сайта Books to Scrape.     
    
    Args:
        book_url (str): Полный URL-адрес страницы книги на сайте Books to Scrape.
                        Например: 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
    
    Парсим HTML-страницу и извлекаю данные:
    название, цену, рейтинг, количество в наличии, описание и дополнительные характеристики
    из таблицы Product Information.

    Returns:
        dict: Словарь с данными о книге. Включает ключи: 'title', 'price', 
              'rating', 'availability', 'description' и поля из таблицы 
              Product Information (например, 'upc', 'product_type', 'tax').
              Если элемент не найден, верну None.
    """

    response = requests.get(book_url)
    response.raise_for_status()
    
    response.encoding = 'utf-8'
    
    soup = BeautifulSoup(response.text, 'html.parser')

    book_data = {}

    title = soup.find('h1')
    book_data['title'] = title.text.strip() if title else None

    price = soup.find('p', class_='price_color')
    book_data['price'] = price.text.strip() if price else None
    
    rating = soup.find('p', class_='star-rating')
    book_data['rating'] = rating.get('class', [None, None])[1] if rating else None
    
    description_div = soup.find('div', id='product_description')
    description_p = description_div.find_next_sibling('p') if description_div else None
    book_data['description'] = description_p.text.strip() if description_p else None

    # Product Information
    table = soup.find('table', class_='table table-striped')
    if table:
        for row in table.find_all('tr'):
            th = row.find('th')
            td = row.find('td')
            if th and td:
                key = th.text.strip().lower().replace(' ', '_')
                value = td.text.strip()
                
                if key == 'availability':
                    start = value.find('(')
                    end = value.find(' ', start)
                    if start != -1 and end != -1:
                        book_data[key] = int(value[start+1:end])
                    else:
                        book_data[key] = value  
                else:
                    book_data[key] = value
                
    return book_data

def scrape_books(is_save: bool = False, max_pages: int = None) -> list:
    """
    Прохожу по страницам каталога сайта Books to Scrape и собираю данные
    
    Использую get_book_data для получения информации о книгах

    Args:
        is_save (bool): Флаг, указывающий, нужно ли сохранять данные 
                        
        max_pages (int): Максимальное число страниц для обхода 
                         По умолчанию None (обходятся все страницы)

    Returns:
        list: Список словарей, где каждый словарь содержит данные об одной книге
    """
    all_books = []
    N = 1
    base_url = 'http://books.toscrape.com/catalogue/'
    
    while True:
        # ДОБАВЛЕНО: Ограничитель для быстрых тестов
        if max_pages is not None and N > max_pages:
            break
            
        catalog_url = f"{base_url}page-{N}.html"
        
        response = requests.get(catalog_url)
        response.raise_for_status()
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'html.parser')
        
        book_articles = soup.find_all('article', class_='product_pod')
        
        for article in book_articles:
            relative_link = article.find('h3').find('a')['href']
            full_book_url = urljoin(base_url, relative_link)
            
            book_data = get_book_data(full_book_url)
            all_books.append(book_data)
            
        next_button = soup.find('li', class_='next')
        if next_button:
            N += 1
            time.sleep(0.2)  # Вежливая задержка
        else:
            break
            
    if is_save:
        with open('books_data.txt', 'w', encoding='utf-8') as f:
            json.dump(all_books, f, ensure_ascii=False, indent=4)
            
    return all_books
