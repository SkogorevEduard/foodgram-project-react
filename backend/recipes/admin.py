from django.contrib import admin

from .models import Recipes


class RecipeIngredientsInLine(admin.TabularInline):
    model = Recipes.ingredients.through
    extra = 1


class RecipeTagsInLine(admin.TabularInline):
    model = Recipes.tags.through
    extra = 1


@admin.register(Recipes)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'text', 'author')
    search_fields = ('name', 'author')
    inlines = (RecipeIngredientsInLine, RecipeTagsInLine)
