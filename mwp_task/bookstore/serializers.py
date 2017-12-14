from rest_framework import serializers

from .models import Book


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


class BookShortForAnonSerializer(BaseBookSerializer):
    authors = serializers.StringRelatedField(many=True)

    class Meta(BaseBookSerializer.Meta):
        fields = ('id', 'name', 'photo', 'authors')


class BookShortForAuthorizedSerializer(BaseBookSerializer):
    authors = serializers.StringRelatedField(many=True)

    class Meta(BaseBookSerializer.Meta):
        fields = ('id', 'name', 'photo', 'authors', 'is_bought')
