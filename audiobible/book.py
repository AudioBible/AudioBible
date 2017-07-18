import os
import json
from kjv import settings

bot_name = settings.BOT_NAME
base_path = os.environ.get('BOOKS_PATH', None)
if not base_path:
    base_path = os.path.expanduser('~')

data_path = os.path.join(os.path.abspath(base_path), settings.DATA_STORE)
content_path = os.path.join(data_path, settings.CONTENT_FILE)


class Books:
    books_info = []
    all_books = []
    collection = set([])

    def __init__(self):
        self.reset()

    def add_book(self, book_name):
        self.collection.add(self.all_books[book_name])

    def reset(self):
        self.collection = set([])

    def _load_books(self):
        if os.path.exists(content_path):
            with open(content_path, 'r') as lines:
                for line in lines:
                    self.books_info.append(json.loads(line))
        for info in self.books_info:
            self.all_books.append({
                'chapters': info['chapters_count'],
                'name': info['name'],
                'text_files': [],
                'audio_files': []
            })
        return self.all_books

if __name__ == '__main__':
    books = Books()
    print(books._load_books())
