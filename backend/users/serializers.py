from djoser.serializers import UserSerializer as DjoserUserSerialiser
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from recipes.models import Recipes

from .models import User


class UserSerializer(DjoserUserSerialiser):
    """Сериализатор для получения информации о пользователе."""
    is_subscribed = serializers.SerializerMethodField(
        method_name='get_is_subscribed'
    )

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.follow.filter(id=obj.id).exists()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_subscribed')


class UserRegistrateSerializer(UserCreateSerializer):
    """Сериализатор для регистрации."""

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'password')


class FollowSerializer(UserSerializer):
    """Сериализатор для работы с информацией о подписках."""
    recipes = serializers.SerializerMethodField(method_name='get_recipes')
    recipes_count = serializers.SerializerMethodField(
        method_name='get_recipes_count'
    )

    def get_serializer(self):
        from recipes.serializers import FollowRecipesShortSerializer

        return FollowRecipesShortSerializer

    def get_recipes(self, obj):
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = Recipes.objects.filter(author=obj)
        if limit:
            recipes = recipes[:int(limit)]
        serializer = self.get_serializer()(recipes,
                                           many=True,
                                           read_only=True)
        return serializer.data

    def get_recipes_count(self, obj):
        return Recipes.objects.filter(author=obj).count()

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name', 'email',
                  'is_subscribed', 'recipes', 'recipes_count')
