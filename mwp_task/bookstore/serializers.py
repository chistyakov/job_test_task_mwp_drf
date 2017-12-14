from rest_framework import serializers

from .models import Book, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', 'surname', 'photo')


class BaseBookSerializer(serializers.ModelSerializer):
    is_bought = serializers.SerializerMethodField()
    link = serializers.SerializerMethodField()

    def get_is_bought(self, obj):
        user = self.context['request'].user
        return user.profile.bought_books.filter(pk=obj.id).exists()

    def get_link(self, obj):
        if self.get_is_bought(obj):
            return obj.link

    class Meta:
        model = Book


authors_short_field = serializers.StringRelatedField(many=True)
authors_detailed_field = AuthorSerializer(read_only=True, many=True)


class BookShortForAnonSerializer(BaseBookSerializer):
    authors = authors_short_field

    class Meta(BaseBookSerializer.Meta):
        fields = ('id', 'name', 'photo', 'authors')


class BookShortForAuthorizedSerializer(BaseBookSerializer):
    authors = authors_short_field

    class Meta(BaseBookSerializer.Meta):
        fields = ('id', 'name', 'photo', 'authors', 'is_bought')


class BookDetailForAnonSerializer(BaseBookSerializer):
    authors = authors_detailed_field

    class Meta(BaseBookSerializer.Meta):
        fields = ('id', 'name', 'photo', 'authors', 'description', 'price')


class BookDetailForAuthorizedSerializer(BaseBookSerializer):
    authors = authors_detailed_field

    class Meta(BaseBookSerializer.Meta):
        fields = '__all__'
