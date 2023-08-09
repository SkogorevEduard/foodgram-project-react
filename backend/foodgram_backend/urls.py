from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

from ingredients.views import IngredientViewSet
from recipes.views import RecipeViewSet
from tags.views import TagViewSet
from users.views import CustomUserViewSet

router = routers.DefaultRouter()
router.register('ingredients', IngredientViewSet)
router.register(r'recipes', RecipeViewSet)
router.register('tags', TagViewSet)
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/', include('djoser.urls')),
    path('api/auth/', include('djoser.urls.authtoken'))
]

if settings.DEBUG:
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
