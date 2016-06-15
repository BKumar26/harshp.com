from django.shortcuts import get_object_or_404
from django.shortcuts import render

from utils.meta_generator import create_meta

# from hobbies.models import Person
from hobbies.models import Author

from hobbies.models import Book
from hobbies.models import BOOK_TYPES
from hobbies.models import BookSeries
from hobbies.models import BookNote
from hobbies.models import BookSeriesNote
from hobbies.models import ReadingList
from hobbies.models import BookQuote


def home(request):
    """Books homepage"""
    # show currently reading books
    now_reading = Book.objects.filter(completed=False, wishlist=False)\
        .order_by('title').select_related('series', 'authors')
    # show wishlist
    wishlist = Book.objects.filter(wishlist=True)\
        .order_by('title').select_related('series', 'authors')
    # show recently finished books
    recently_finished = Book.objects.filter(wishlist=False, completed=True)\
        .order_by('-date_end', 'title').select_related('series', 'authors')
    # show reading lists
    reading_lists = ReadingList.objects.order_by('name')
    # book quotes
    quotes = BookQuote.objects.order_by('-pk').select_related('book')

    meta = create_meta(
        title='hobbies.harshp.com',
        description='hobbies for harshp.com',
        keywords=['hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/books/home.html',
        {
            'meta': meta,
            'reading': now_reading,
            'wishlist': wishlist,
            'recent': recently_finished,
            'lists': reading_lists,
            'quotes': quotes
        })


def _filter_by_book_type(book_type=None, filters=None, ordering=None):
    """apply filters on books"""
    context = 'Books' if book_type is None else BOOK_TYPES[book_type] + 's'
    if book_type is not None and filters is None:
        filters = {'book_type': BOOK_TYPES[book_type]}
    elif book_type is not None and filters is not None:
        filters['book_type'] = BOOK_TYPES[book_type]

    if filters is not None:
        books = Book.objects.filter(**filters)
    else:
        books = Book.objects

    if ordering is not None:
        books = books.order_by(*ordering)

    books = books.select_related('author', 'author__person', 'series')

    return context, books


def order_title(request, book_type=None):
    """Books ordered by title"""
    context, books = _filter_by_book_type(
        book_type, filters=None, ordering=['title'])

    meta = create_meta(
        title='books ordered by title',
        description='reading as a hobby',
        keywords=['books', 'hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/books/list.html',
        {
            'meta': meta,
            'type': context,
            'title': 'ordered by title',
            'books': books,
        })


def order_read(request, book_type=None):
    """Books ordered by date read or completed"""
    context, books = _filter_by_book_type(
        book_type, filters={'wishlist': False},
        ordering=['-completed', '-date_end', 'title'])

    meta = create_meta(
        title='books ordered by date completed',
        description='reading as a hobby',
        keywords=['books', 'hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/books/list.html',
        {
            'meta': meta,
            'type': context,
            'title': 'ordered by date completed',
            'books': books,
        })


def order_rating(request, book_type=None):
    """Books ordered by rating"""
    context, books = _filter_by_book_type(
        book_type,
        filters={'wishlist': False, 'completed': False},
        ordering=['-rating', 'title'])

    meta = create_meta(
        title='books ordered by rating',
        description='reading as a hobby',
        keywords=['books', 'hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/books/list.html',
        {
            'meta': meta,
            'type': context,
            'title': 'ordered by rating',
            'books': books,
        })


def wishlist(request, book_type=None):
    """Books in my wishlist"""
    context, books = _filter_by_book_type(
        book_type, filters={'wishlist': True}, ordering=['title'])

    meta = create_meta(
        title='wishlist of books to read',
        description='reading as a hobby',
        keywords=['books', 'hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/books/list.html',
        {
            'meta': meta,
            'type': context,
            'title': 'wishlist',
            'books': books,
        })


def favorites(request, book_type=None):
    """Favorite Books"""
    context, books = _filter_by_book_type(
        book_type,
        filters={'wishlist': False, 'completed': True, 'favorite': True},
        ordering=['title'])

    meta = create_meta(
        title='favorite books',
        description='reading as a hobby',
        keywords=['books', 'hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/books/list.html',
        {
            'meta': meta,
            'type': context,
            'title': 'ordered by rating',
            'books': books,
        })


def series(request, book_type=None):
    """Book Series"""
    if book_type is not None:
        book_type = 'Book'
        series = BookSeries.objects
    else:
        series = BookSeries.objects.filter(book_type=BOOK_TYPES['Novel'])
    series = series.order_by('title').prefetch('books', 'notes')

    meta = create_meta(
        title='book series',
        description='reading as a hobby',
        keywords=['books', 'hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/books/series_list.html',
        {
            'meta': meta,
            'type': book_type + 's',
            'series': series,
        })


def series_favorites(request, book_type=None):
    """Favorite Book Series"""
    if book_type is not None:
        book_type = 'Book'
        series = BookSeries.objects.filter(favorite=True)
    else:
        series = BookSeries.objects\
            .filter(book_type=BOOK_TYPES['Novel'], favorite=True)
    series = series.order_by('title').prefetch('books', 'notes')

    meta = create_meta(
        title='favorite book series',
        description='reading as a hobby',
        keywords=['books', 'hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/books/series_list.html',
        {
            'meta': meta,
            'type': 'Favorite {}s'.format(book_type),
            'series': series,
        })


def book(request, book_slug):
    """Return a particular book."""
    book = get_object_or_404(
        Book.objects
            .select_related('author', 'author__person', 'series')
            .prefetch_related('reading_lists', 'notes'),
        slug=book_slug)
    return render(
        request, 'hobbies/books/book.html',
        {
            'book': book,
        })


def book_note(request, book_slug, note_slug):
    """Book Note"""
    post = get_object_or_404(
        BookNote.objects.select_related('book'),
        book__slug=book_slug, slug=note_slug)
    return render(
        request, 'hobbies/books/note.html',
        {
            'post': post,
        })


def series_note(request, series_slug, note_slug):
    """Book Series Note"""
    post = get_object_or_404(
        BookSeriesNote.objects.select_related('series')
        .prefetch_related('series__books'),
        series__slug=series_slug, slug=note_slug)
    return render(
        request, 'hobbies/books/series_note.html',
        {
            'post': post,
        })


def authors(request):
    """Authors"""
    authors = Author.objects\
        .order_by('person__name').prefetch_related('books')

    meta = create_meta(
        title='authors',
        description='reading as a hobby',
        keywords=['author', 'books', 'hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/books/authors.html',
        {
            'meta': meta,
            'title': 'Authors',
            'authors': authors,
        })


def authors_favorite(request):
    """Favorite Authors"""
    authors = Author.objects.filter(favorite=True)\
        .order_by('person__name').prefetch_related('books')

    meta = create_meta(
        title='favorite authors',
        description='reading as a hobby',
        keywords=['author', 'books', 'hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/books/authors.html',
        {
            'meta': meta,
            'title': 'Favorite Authors',
            'authors': authors,
        })


def author(request, person_slug):
    """Author"""
    author = get_object_or_404(
        Author.objects.select_related('person').prefetch_related('books'),
        person__slug=person_slug)
    return render(
        request, 'hobbies/books/author.hmtl',
        {
            'author': author,
        })


def reading_lists(request):
    """Reading Lists"""
    reading_lists = ReadingList.objects\
        .order_by('name').prefetch_related('entries')

    meta = create_meta(
        title='reading lists',
        description='reading as a hobby',
        keywords=['books', 'hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/book/reading_lists.html',
        {
            'meta': meta,
            'lists': reading_lists,
        })


def reading_list(request, list_slug):
    """Reading List"""
    reading_list = get_object_or_404(
        ReadingList.objects.order_by('title').prefetch_related('entries'))
    return render(
        request, 'hobbies/books/reading_list.html',
        {
            'reading_list': reading_list,
        })


def quotes(request):
    """Quotes"""
    quotes = BookQuote.objects.order_by('-pk').select_related('book')

    meta = create_meta(
        title='book quotes',
        description='reading as a hobby',
        keywords=['books', 'quote', 'hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/book/quotes.html',
        {
            'meta': meta,
            'title': 'Quotes',
            'quotes': quotes,
        })


def quotes_favorite(request):
    """Favorite Quotes"""
    quotes = BookQuote.objects.filter(favorite=True)\
        .order_by('-pk').select_related('book')

    meta = create_meta(
        title='book quotes',
        description='reading as a hobby',
        keywords=['books', 'quote', 'hobbies', 'harshp.com'],
        url=request.build_absolute_url())

    return render(
        request, 'hobbies/book/quotes.html',
        {
            'meta': meta,
            'title': 'Favorite Quotes',
            'quotes': quotes,
        })


def quote(request, pk):
    """Quote"""
    quote = get_object_or_404(
        BookQuote.select_related('book', 'book__author__person', pk=pk))
    return render(
        request, 'hobbies/book/quote.html',
        {
            'quote': quote,
        })
