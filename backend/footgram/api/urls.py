from django.urls import include, path
from rest_framework import routers

from .ingredients.views import IngredientViewSet
from .recipes.views import RecipeViewSet
from .tags.views import TagViewSet
from .users.views import CustomUserViewSet

app_name = 'api'

router = routers.DefaultRouter()
router.register('users', CustomUserViewSet)
router.register('tags', TagViewSet)
router.register('ingredients', IngredientViewSet)
router.register('recipes', RecipeViewSet)

djoser = [
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]

urlpatterns = [
    path('', include(router.urls)),
    path('', include(djoser)),
]
