from django.shortcuts import render


def index(request):
    names = "john,doe,mark,swain"
    return render(request, 'index.html', {'names': names})

def greeting_view(request):
    books = {
        "The Great Gatsby": "F. Scott Fitzgerald",
        "To Kill a Mockingbird": "Harper Lee",
        "1984": "George Orwell",
        "Pride and Prejudice": "Jane Austen"
    }
    context = {
        'username': 'Jdoe',
        'books': books
    }
    return render(request, 'simple_tag_template.html', context)
