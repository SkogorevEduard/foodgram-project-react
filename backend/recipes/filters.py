from django_filters import rest_framework, filters, FilterSet

from tags.models import Tag

from .models import Recipes


class RecipeFilter(FilterSet):
    is_favorited = filters.BooleanFilter(
        method='get_is_favorited'
    )
    is_in_shopping_list = filters.BooleanFilter(
        method='get_is_in_shopping_list'
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

    def get_is_favorited(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorite_recipes__user=self.request.user)
        return queryset

    def get_is_in_shopping_list(self, queryset, name, value):
        if self.request.user.is_authenticated and value:
            return queryset.filter(shopping_cart_recipes__user=self.request.user)
        return queryset

    class Meta:
        model = Recipes
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_list')
