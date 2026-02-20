from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('recipes/', views.recipe_list, name='recipe_list'),
    path('recipe/<int:pk>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/new/', views.recipe_create, name='recipe_create'),
    path('recipe/<int:pk>/edit/', views.recipe_update, name='recipe_update'),
    path('recipe/<int:pk>/delete/', views.recipe_delete, name='recipe_delete'),
    path('recipe/<int:pk>/like/', views.like_recipe, name='like_recipe'),
    path('profile/', views.profile, name='profile'),
    path('profile/update/', views.profile_update, name='profile_update'),
    path('signup/', views.signup, name='signup'),
    path('search/', views.search_recipes, name='search'),
    path('category/<int:category_id>/', views.category_recipes, name='category_recipes'),
    path('recipe/external/', views.recipe_detail_external, name='recipe_external'),
    # ===== NEW URL =====
    path('saved-recipes/', views.saved_recipes, name='saved_recipes'),  # 👈 Add this line
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('terms/', views.terms, name='terms'),
    path('privacy/', views.privacy, name='privacy'),
]