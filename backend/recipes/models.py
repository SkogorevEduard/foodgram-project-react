from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Exists, OuterRef

from ingredients.models import Ingredient
from tags.models import Tag
from users.models import User


class CustomQuerySet(models.QuerySet):
    """Класс для добавления избранного и списка корзины."""

    def add_annotations(self, user):
        return self.annotate(
            is_favorited=Exists(
                user.favorite_recipes.filter(
                    id=OuterRef('id')
                )
            ),
            is_in_shopping_cart=Exists(
                user.shopping_cart_recipes.filter(
                    id=OuterRef('id')
                )
            ),
        )


class Recipes(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название',
    )
    image = models.ImageField(
        verbose_name='Изображение для рецепта',
        upload_to='recipes/',
    )
    text = models.TextField(
        verbose_name='Описание рецепта',
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        related_name='recipes',
        verbose_name='Игредиенты для рецепта',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTag',
        related_name='recipes',
        verbose_name='Теги рецепта',
    )
    favorites = models.ManyToManyField(
        User,
        verbose_name='Избранное',
        blank=True,
        related_name='favorite_recipes',
    )
    shopping_carts = models.ManyToManyField(
        User,
        verbose_name='Список покупок',
        blank=True,
        related_name='shopping_cart_recipes',
    )
    cooking_time = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Время приготовления (в минутах)',
    )

    objects = CustomQuerySet.as_manager()

    class Meta:
        ordering = ['-id']
        verbose_name = 'рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name='Ингредиент'
    )
    amount = models.PositiveSmallIntegerField(
        validators=(MinValueValidator(1),),
        verbose_name='Количество'
    )

    class Meta:
        verbose_name = 'ингредиент'
        verbose_name_plural = 'Ингредиенты'


class RecipeTag(models.Model):
    recipe = models.ForeignKey(
        Recipes,
        on_delete=models.CASCADE,
        verbose_name='Рецепт'
    )
    tag = models.ForeignKey(
        Tag,
        on_delete=models.CASCADE,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'тег'
        verbose_name_plural = 'Теги'
