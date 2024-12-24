from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.utils import timezone
from django.core.files.images import ImageFile
from django.core.exceptions import PermissionDenied
from django.http import FileResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book, Review, Contributor, Publisher
from .utils import average_rating
from .forms import SearchForm, PublisherForm, ReviewForm, BookMediaForm
from PIL import Image
from io import BytesIO


def is_staff_user(user):
    return user.is_staff


def sample_download(request, book_pk):
    book = get_object_or_404(Book, pk=book_pk)
    sample = book.sample
    return FileResponse(open(sample.path, 'rb'), as_attachment=True)


@login_required
def book_media(request, book_pk):
    book = Book.objects.get(pk=book_pk)
    if request.method == 'POST':
        form = BookMediaForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            book = form.save(False)
            uploaded_image = form.cleaned_data['cover']
            if uploaded_image and not hasattr(uploaded_image, 'path'):
                image = Image.open(uploaded_image)
                image.thumbnail((300, 300))
                image_data = BytesIO()
                image.save(fp=image_data, format=image.format)
                image_file = ImageFile(image_data)
                book.cover.save(uploaded_image.name, image_file)
                book.sample = form.cleaned_data['sample']
                messages.success(request, f'Book {book} was successfully updated.')
            book.save()
            return redirect('book_details', book_pk)
    else:
        form = BookMediaForm(instance=book)
    context = {
        'form': form,
        'instance': book,
        'model_type': 'Book',
        'is_file_upload': True
    }
    return render(request, "reviews/instance-form.html", context)


@login_required
def review_edit(request, book_pk, review_pk=None):
    book = get_object_or_404(Book, pk=book_pk)
    if review_pk is None:
        review = None
    else:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)
        user = request.user
        if not user.is_staff and review.creator.id != user.id:
            raise PermissionDenied
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            updated_review = form.save(False)
            if review is None:
                updated_review.book_id = book_pk
                messages.success(request, f'Review for "{book}" was created.')
                updated_review.save()
            else:
                messages.success(request, f'Review for "{book}" was updated.')
                updated_review.date_edited = timezone.now()
                updated_review.save()
            return redirect('book_details', book_pk)
    else:
        form = ReviewForm(instance=review)
    context = {
        'form': form,
        'instance': review,
        'model_type': 'Review',
        'related_model_type': 'Book',
        'related_instance': book
    }
    return render(request, "reviews/instance-form.html", context)


@user_passes_test(is_staff_user)
def publisher_edit(request, pk=None):
    if pk is not None:
        publisher = get_object_or_404(Publisher, pk=pk)
    else:
        publisher = None
    if request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            updated_publisher = form.save()
            if publisher is None:
                messages.success(request, f'Publisher {updated_publisher} was created.')
            else:
                messages.success(request, f'Publisher {updated_publisher} was updated.')
            return redirect('publisher_edit', updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)
    context = {
        'form': form,
        'instance': publisher,
        'model_type': 'Publisher'
    }
    return render(request, "reviews/instance-form.html", context)


def index(request):
    return render(request, 'reviews/base.html')


def search1(request):
    query = request.GET.get('search')
    context = {
        'search': query
    }
    return render(request, 'reviews/search1.html', context)


def book_search(request):
    search = request.GET.get('search', '')
    search_history: [list] = request.session.get('search_history', [])
    search_in = 'title'
    contributor = ''
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            search = dict(form.cleaned_data.items())['search']
            search_in = dict(form.cleaned_data.items())['search_in']
            if request.user.is_authenticated:
                searched = [search, search_in]
                if searched in search_history:
                    search_history.pop(search_history.index(searched))
                search_history.insert(0, searched)
                search_history = search_history[:10]
                request.session['search_history'] = search_history
    elif search_history:
        initial = dict(search=search, search_in=search_history[0][1])
        form = SearchForm(initial=initial)
    else:
        form = SearchForm()
    if search == '':
        books = []
    else:
        if search_in == 'title':
            books = Book.objects.filter(title__icontains=search)

        else:
            contributors = Contributor.objects.filter(Q(first_names__icontains=search) |
                                                      Q(last_names__icontains=search))
            if contributors:
                books = []
                for contributor in contributors:
                    contrib_books = contributor.book_set.all()
                    for book in contrib_books:
                        books.append(book)
            else:
                books = []

    context = {
        'form': form,
        'books': books,
        'search_text': search,
        'contributor': contributor
    }

    return render(request, 'reviews/search-results.html', context)


def book_list(request):
    books = Book.objects.all()
    book_list = []
    for book in books:
        reviews = book.review_set.all()
        if reviews:
            rating_list = [review.rating for review in reviews]
            book_rating = average_rating(rating_list)
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append({'book': book,
                          'book_rating': book_rating,
                          'number_of_reviews': number_of_reviews})
    context = {'book_list': book_list}
    return render(request, 'reviews/book_list.html', context)


def book_details(request, pk):
    book = Book.objects.get(id=pk)
    reviews = book.review_set.all()
    if reviews:
        rating_list = [review.rating for review in reviews]
        book_rating = average_rating(rating_list)
    else:
        book_rating = None
    if request.user.is_authenticated:
        max_viewed_books: [int] = 10
        viewed_books: [list] = request.session.get('viewed_books', [])
        viewed_book = [book.id, book.title]
        if viewed_book in viewed_books:
            viewed_books.pop(viewed_books.index(viewed_book))
        viewed_books.insert(0, viewed_book)
        viewed_books = viewed_books[:max_viewed_books]
        request.session['viewed_books'] = viewed_books
    context = {
        'book': book,
        'book_rating': book_rating,
        'reviews': reviews
    }
    return render(request, 'reviews/book_details.html', context)
