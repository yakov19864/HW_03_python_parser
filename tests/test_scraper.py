"""Автотесты"""

import sys
import os

from scraper import get_book_data, scrape_books

BOOK_URL = (
    'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'
)

def test_get_book_data_keys():
    """данные о книге возвращаются в виде словаря с нужными ключами"""
    book_data = get_book_data(BOOK_URL)
    assert isinstance(book_data, dict)
    assert {'title', 'price', 'rating', 'availability', 'description'} <= book_data.keys()

def test_scrape_books_count():
    """количество собранных книг соответствует ожиданиям (20 шт) """
    books = scrape_books(is_save=False, max_pages=1)
    assert isinstance(books, list)
    assert len(books) == 20

def test_get_book_data_values():
    """значения отдельных полей (например, `title`) корректны"""
    book_data = get_book_data(BOOK_URL)
    assert book_data['title'] == 'A Light in the Attic'  # конкретная книга
    
    assert book_data['price'].startswith('£')
    assert book_data['rating'] in ['One', 'Two', 'Three', 'Four', 'Five']
    assert isinstance(book_data['availability'], int)
    assert book_data['availability'] > 0
