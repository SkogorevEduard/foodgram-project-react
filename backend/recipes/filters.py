from django_filters import FilterSet
from django_filters import rest_framework as filters
from rest_framework import filters as rest_framework_filters

from tags.models import Tag

from .models import Recipes


class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter()
    is_in_shopping_cart = filters.BooleanFilter()
    author = filters.NumberFilter(
        field_name='author',
        lookup_expr='exact'
    )
    tags = filters.ModelMultipleChoiceFilter(
        field_name='tags__slug',
        to_field_name='slug',
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Recipes
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')


class IngredientsSearchFilter(rest_framework_filters.SearchFilter):
    search_param = 'name'
