from django.db.models import Sum

from .models import RecipeIngredient
from ingredients.models import Ingredient


def recipe_amount_ingredients_bulk(recipes, ingredients):
    RecipeIngredient.objects.bulk_create([RecipeIngredient(
        recipe=recipes,
        ingredient=Ingredient.objects.get(id=ingredient['id']),
        amount=ingredient['amount']
    ) for ingredient in ingredients])


def get_shopping_list(user):
    buy_list = RecipeIngredient.objects.filter(
        recipe__in=(user.shopping_cart_recipes.values('id'))
    ).values(
        'ingredient'
    ).annotate(
        amount=Sum('amount')
    )
    buy_list_text = 'Список покупок:\n\n'
    for item in buy_list:
        ingredient = Ingredient.objects.get(pk=item['ingredient'])
        amount = item['amount']
        buy_list_text += (
            f'{ingredient.name}, {amount} '
            f'{ingredient.measurement_unit}\n'
        )
    return buy_list_text
