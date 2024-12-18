from django.shortcuts import render
from django.conf.urls import handler404
from django.urls import path

from project_supermarket.web.views import Home, Dashboard, Register, Login, EditProfile, Basket, AboutUs, CreateProduct, \
    ProductDetails, EditProduct, Recipes, CreateRecipe, RecipeDetails, EditRecipe, Logout, DeleteProfile, DeleteProduct, \
    DeleteRecipe

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('dashboard/', Dashboard.as_view(), name='dashboard'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
    path('profile/<int:pk>/edit/', EditProfile.as_view(), name='edit profile'),
    path('profile/<int:pk>/delete', DeleteProfile.as_view(), name='delete profile'),
    #path('profile/details', ProfileDetails.as_view(), name='profile details'),
    path('basket/', Basket.as_view(), name='basket'),
    path('about-us/', AboutUs.as_view(), name='about us'),
    path('product/create/', CreateProduct.as_view(), name='create product'),
    path('product/<slug:product_slug>/details/', ProductDetails.as_view(), name='product details'),
    path('product/<slug:product_slug>/edit/', EditProduct.as_view(), name='edit product'),
    path('product/<slug:product_slug>/delete/', DeleteProduct.as_view(), name='delete product'),
    path('recipes/', Recipes.as_view(), name='recipes'),
    path('recipe/create/', CreateRecipe.as_view(), name='create recipe'),
    path('recipe/<int:pk>/details/', RecipeDetails.as_view(), name='recipe details'),
    path('recipe/<int:pk>/edit/', EditRecipe.as_view(), name='edit recipe'),
    path('recipe/<int:pk>/delete', DeleteRecipe.as_view(), name='delete recipe'),
]


def custom_404(request, exception):
    return render(request, '404.html', status=404)


handler404 = custom_404
