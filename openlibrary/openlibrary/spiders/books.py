# -*- coding: utf-8 -*-
import scrapy
import json

class BooksSpider(scrapy.Spider):
    name = 'books'
    allowed_domains = ['openlibrary.org']
    start_urls = ['https://openlibrary.org/subjects/picture_books.json?limit=12&offset=0']

    page_num = 0
    page_step = 12

    def parse(self, response):
        resp = json.loads(response.body)
        books = resp.get('works')

        ebook_count = resp.get('ebook_count')
        
        for book in books:
            cover_url =str(book.get('cover_id'))+'.jpg'
            yield{
                'title': book.get('title'),
                'author': [sub['name'] for sub in book.get('authors')], 
                'author_link':  [response.urljoin(sub['key']) for sub in book.get('authors')] , 
                'cover_edition_key': book.get('cover_edition_key'), 
                'image_url': f'https://covers.openlibrary.org/b/id/{cover_url}', 
                'edition_count': book.get('edition_count'), 
                'first_publish_year': book.get('first_publish_year'), 
                'has_fulltext': book.get('has_fulltext'), 
                'book_url': response.urljoin(book.get('key')), 
                'subject': book.get('subject')
            }
        self.page_num += self.page_step
        
        if self.page_num < ebook_count:
            yield scrapy.Request(
                url=f'https://openlibrary.org/subjects/picture_books.json?limit=12&offset={self.page_num}',
                callback=self.parse
            )
