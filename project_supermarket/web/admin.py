from django.contrib import admin

from project_supermarket.web.models import User, Cooker, Product, Recipe, SpecialOffers


@admin.register(SpecialOffers)
class SpecialOffersAdmin(admin.ModelAdmin):
    list_display = ('offer_name', 'offer_type', 'bundle_discount', 'start_date', 'end_date', 'active')
    list_filter = ('products',)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    exclude = ('last_login',)


@admin.register(Cooker)
class CookerAdmin(admin.ModelAdmin):
    list_display = ('name', 'speciality', 'age')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    exclude = ('slug',)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('ingredients', 'recipe', 'product', 'chef')
