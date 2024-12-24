import datetime

from django.db.models import Count
from reviews.models import Review


def get_books_read_by_month(username: [str]):
    """Get the books read by the user on per month basis.
    :param: str The username for which the books needs
    to be returned
    :return: dict of month wise books read
    """
    current_year = datetime.datetime.now().year
    books = Review.objects.filter(
        creator__username__contains=username,  # creator's username contains 'username'
        date_created__year=current_year  # Filters reviews created in the current year
    ).values('date_created__month').annotate(book_count=Count('book__title'))
    # values Выводит словарь значений вместо объектов
    # values('date_created__month') Groups the filtered results by the month part of the date_created field.
    # annotate(book_count=Count('book__title'))
    # До кожної групи додається кількість записів book__title у цій групі,
    # що фактично підраховує кількість книжок, переглянутих щомісяця.
    return books


