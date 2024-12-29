import pytest
from main import BooksCollector

# класс TestBooksCollector объединяет набор тестов, которыми мы покрываем наше приложение BooksCollector
# обязательно указывать префикс Test

@pytest.fixture
def collector():
    return BooksCollector()

TEST_BOOK_NAME = 'Как перестать прокрастинировать?'
TEST_BOOK_PART_2_NAME = f"{TEST_BOOK_NAME} часть 2"
TEST_GENRE = 'Ужасы'

@pytest.fixture
def collector_book(collector):
    collector.add_new_book(TEST_BOOK_NAME)
    collector.add_new_book(TEST_BOOK_PART_2_NAME)

    return collector

@pytest.fixture
def collector_book_by_genre(collector_book):
    for book in collector_book.get_books_genre():
        collector_book.set_book_genre(book, TEST_GENRE)

    return collector_book

@pytest.fixture
def collector_favorites(collector_book):
    collector_book.add_book_in_favorites(TEST_BOOK_NAME)

    return collector_book

class TestBooksCollector:

    # пример теста:
    # обязательно указывать префикс test_
    # дальше идет название метода, который тестируем add_new_book_
    # затем, что тестируем add_two_books - добавление двух книг
    def test_add_new_book_add_two_books(self, collector):
        # добавляем две книги
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')

        # проверяем, что добавилось именно две
        # словарь books_rating, который нам возвращает метод get_books_rating, имеет длину 2
        assert len(collector.get_books_genre()) == 2

    # напиши свои тесты ниже
    # чтобы тесты были независимыми в каждом из них создавай отдельный экземпляр класса BooksCollector()

    def test_add_new_book_no_genre(self, collector):
        TEST_NAME = 'Гордость и предубеждение и зомби'
        collector.add_new_book(TEST_NAME)
        assert collector.get_book_genre(TEST_NAME) == ''

    def test_set_book_genre(self, collector_book):
        collector_book.set_book_genre(TEST_BOOK_NAME, TEST_GENRE)
        assert collector_book.get_book_genre(TEST_BOOK_NAME) == TEST_GENRE

    def test_get_book_genre(self, collector_book_by_genre):
        assert collector_book_by_genre.get_book_genre(TEST_BOOK_NAME) == TEST_GENRE

    @pytest.mark.parametrize(
            'books, genre',
            [
                ['Book 1,Book 2', 'Ужасы'],
                ['Book 3,Book 4', 'Фантастика']
            ]

        )
    def test_get_books_with_specific_genre(self, collector, books, genre):
        book_list = books.split(',')
        for book in book_list:
            collector.add_new_book(book)
            collector.set_book_genre(book, genre)

        assert len(collector.get_books_with_specific_genre(genre)) == 2

    def test_get_books_genre(self, collector_book):
        assert len(collector_book.get_books_genre()) == 2

    def test_get_books_for_children(self, collector_book):
        collector_book.set_book_genre(TEST_BOOK_NAME, 'Мультфильмы')
        assert len(collector_book.get_books_for_children()) == 1

    def test_add_get_book_in_favorites(self, collector_favorites):
        collector_favorites.add_book_in_favorites(TEST_BOOK_PART_2_NAME)
        assert len(collector_favorites.get_list_of_favorites_books()) == 2

    def test_delete_get_book_from_favorites(self, collector_favorites):
        collector_favorites.delete_book_from_favorites(TEST_BOOK_NAME)
        assert len(collector_favorites.get_list_of_favorites_books()) == 0