from distutils.util import strtobool

from django_filters import rest_framework, filters, FilterSet

from ingredients.models import Ingredient
from tags.models import Tag

from .models import Favorite, Recipes, ShoppingList

CHOICES_LIST = (
    ('0', 'False'),
    ('1', 'True')
)


class RecipeFilter(rest_framework.FilterSet):
    is_favorited = rest_framework.ChoiceFilter(
        choices=CHOICES_LIST,
        method='is_favorited_method'
    )
    is_in_shopping_list = rest_framework.ChoiceFilter(
        choices=CHOICES_LIST,
        method='is_in_shopping_list_method'
    )
    author = rest_framework.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    tags = rest_framework.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    def is_favorited_method(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipes.objects.none()
        favorites = Favorite.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in favorites]
        new_queryset = queryset.filter(id__in=recipes)
        if not strtobool(value):
            return queryset.difference(new_queryset)
        return queryset.filter(id__in=recipes)

    def is_in_shopping_list_method(self, queryset, name, value):
        if self.request.user.is_anonymous:
            return Recipes.objects.none()
        shopping_list = ShoppingList.objects.filter(user=self.request.user)
        recipes = [item.recipe.id for item in shopping_list]
        new_queryset = queryset.filter(id__in=recipes)
        if not strtobool(value):
            return queryset.difference(new_queryset)
        return queryset.filter(id__in=recipes)

    class Meta:
        model = Recipes
        fields = ('author', 'tags')


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )
