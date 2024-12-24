from django import template
from django.contrib.auth.models import User

register = template.Library()
from plotly.offline import plot
import plotly.graph_objs as graphs


@register.inclusion_tag('user_book_list.html')  # цей шаблон буде вставлен в інший шаблон
def book_list(username):
    user = User.objects.get(username=username)  # retrieve user from User model
    reviews = user.review_set.all()  # retrieve all reviews for user
    book_list = [review.book.title for review in reviews]  # retrieve all books from user reviews
    return {'book_list': book_list}


@register.inclusion_tag('temp-plot.html')
def plot_demo():
    figure = graphs.Figure()
    scatter = graphs.Scatter(x=[1, 2, 3, 4, 5], y=[3, 8, 7, 9, 2])
    figure.add_trace(scatter)
    plot_demo = plot(figure, output_type='div')
    return {'plot_demo': plot_demo}
