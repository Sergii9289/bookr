from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework import serializers
from rest_framework.exceptions import NotAuthenticated, PermissionDenied
from .models import Book, Publisher, Review
from .utils import average_rating


class PublisherSerializer(serializers.ModelSerializer):
    pass


class PublisherSerializer(serializers.ModelSerializer):
    class Meta:
        model = Publisher
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']


class ReviewSerializer(serializers.ModelSerializer):
    creator = UserSerializer(read_only=True)
    book = serializers.StringRelatedField(read_only=True)  # retrieve __str_ method from Book instance

    class Meta:
        model = Review
        fields = ['pk', 'content', 'date_created', 'date_edited', 'rating', 'creator', 'book', 'book_id']

        def create(self, validated_data):
            request = self.context['request']
            creator = request.user
            if not creator.is_authenticated:
                raise NotAuthenticated('Authentication required.')
            book = Book.objects.get(pk=request.data['book_id'])
            return Review.objects.create(content=validated_data['content'], book=book, creator=creator,
                                         rating=validated_data['rating'])

        def update(self, instance, validated_data):
            request = self.context['request']
            creator = request.user
            if not creator.is_authenticated or instance.creator_id != creator.pk:
                raise PermissionDenied('Permission denied, you are not the creator of this review')
            instance.content = validated_data['content']
            instance.rating = validated_data['rating']
            instance.date_edited = timezone.now()
            instance.save()
            return instance


class BookSerializer(serializers.ModelSerializer):
    publisher = PublisherSerializer()
    rating = serializers.SerializerMethodField('book_rating')  # returns result of 'book_rating' function
    reviews = serializers.SerializerMethodField('book_reviews')  # returns result of 'book_review' function

    def book_rating(self, book):
        reviews = book.review_set.all()
        if reviews:
            return average_rating([review.rating for review in reviews])

    def book_reviews(self, book):
        reviews = book.review_set.all()
        if reviews:
            return ReviewSerializer(reviews, many=True).data

    class Meta:
        model = Book
        fields = ['title', 'publication_date', 'isbn', 'publisher', 'rating', 'reviews']



# class ContributionSerializer(serializers.ModelSerializer):
#     book = BookSerializer()
#
#     class Meta:
#         model = BookContributor
#         fields = ['book', 'role']
#
# #
# class ContributorSerializer(serializers.ModelSerializer):
#     bookcontributor_set = ContributionSerializer(many=True) # тільки така назва поля!!!
#     number_contributions = serializers.ReadOnlyField() # bookcontributor_set передається в функцію
#
#     class Meta:
#         model = Contributor
#         fields = ['first_names', 'last_names', 'email', 'bookcontributor_set', 'number_contributions']