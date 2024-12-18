from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

from django.contrib.auth.base_user import AbstractBaseUser
from django.core.validators import MinLengthValidator
from django.db import models
from django.utils.text import slugify

from project_supermarket.web.managers import SupermarketEmiUserManager
from project_supermarket.web.validators import contains_only_letters_validator


class User(AbstractBaseUser, PermissionsMixin):
    MAX_NAME_LENGTH = 30
    MIN_NAME_LENGTH = 2

    first_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=[
            MinLengthValidator(MIN_NAME_LENGTH),
            contains_only_letters_validator,
        ],
        null=True,
        blank=True,

    )
    last_name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=[
            MinLengthValidator(MIN_NAME_LENGTH),
            contains_only_letters_validator,
        ],
        null=True,
        blank=True,
    )
    email = models.EmailField(
        unique=True,
    )
    date_of_birth = models.DateField(
        null=True,
        blank=True,
    )
    is_staff = models.BooleanField(
        default=False,
    )
    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = 'email'

    objects = SupermarketEmiUserManager()


class Cooker(models.Model):
    MAX_NAME_LENGTH = 20
    MIN_NAME_LENGTH = 2
    MAX_SPECIALITY_LENGTH = 30

    name = models.CharField(
        max_length=MAX_NAME_LENGTH,
        validators=(
            contains_only_letters_validator,
            MinLengthValidator(MIN_NAME_LENGTH),
        ),
        null=False,
        blank=False,
    )
    speciality = models.CharField(
        max_length=MAX_SPECIALITY_LENGTH,
        null=True,
        blank=True,
    )
    age = models.IntegerField(
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORIES = (
        ('salad', 'salad'),
        ('main', 'main'),
        ('desert', 'desert'),
        ('breakfast', 'breakfast')
    )
    MAX_CATEGORIES_LENGTH = max(len(category) for category, _ in CATEGORIES)

    MAX_PRODUCT_NAME_LENGTH = 50
    MIN_PRODUCT_NAME_LENGTH = 2

    MAX_PRICE_DIGITS = 5
    MAX_PRICE_DECIMAL_PLACES = 2

    MAX_COOKER_NAME_LENGTH = 30
    MIN_COOKER_NAME_LENGTH = 2

    MAX_DESCRIPTION_LENGTH = 500

    name = models.CharField(
        max_length=MAX_PRODUCT_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_PRODUCT_NAME_LENGTH),
        ),
        null=False,
        blank=False,
    )
    price = models.DecimalField(
        max_digits=MAX_PRICE_DIGITS,
        decimal_places=MAX_PRICE_DECIMAL_PLACES,
        null=False,
        blank=False,
    )
    category = models.CharField(
        max_length=MAX_CATEGORIES_LENGTH,
        choices=CATEGORIES,
        blank=True,
        null=True,
    )
    description = models.TextField(
        max_length=MAX_DESCRIPTION_LENGTH,
        null=False,
        blank=False,
    )
    cooker = models.ForeignKey(
        Cooker,
        on_delete=models.DO_NOTHING,
        related_name='cooker',
        null=False,
        blank=False,
    )
    picture = models.URLField()
    slug = models.SlugField(
        unique=True,
        null=False,
        blank=True,
        editable=False,
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.slug:
            self.slug = slugify(f'{self.name}-{self.pk}')
        super().save(*args, **kwargs)


class SpecialOffers(models.Model):
    OFFER_TYPES = (
        ('percentage', 'percentage'),
        ('flat', 'flat discount'),
    )
    MAX_OFFER_TYPES_LENGTH = max(len(offer_type) for offer_type, _ in OFFER_TYPES)

    MAX_OFFER_NAME_LENGTH = 255
    MIN_OFFER_NAME_LENGTH = 2

    MAX_BUNDLE_DISCOUNT_DIGITS = 6
    MAX_BUNDLE_DISCOUNT_DECIMAL_PLACES = 2
    BUNDLE_DISCOUNT_DEFAULT = 0

    offer_name = models.CharField(
        max_length=MAX_OFFER_NAME_LENGTH,
        validators=(
            MinLengthValidator(MIN_OFFER_NAME_LENGTH),
        ),
        null=False,
        blank=False,
    )
    products = models.ManyToManyField(
        Product,
        related_name='products_included',
    )
    products_count = models.PositiveIntegerField(
        default=0,
    )
    offer_type = models.CharField(
        max_length=MAX_OFFER_TYPES_LENGTH,
        choices=OFFER_TYPES,
        null=False,
        blank=False,
    )
    bundle_discount = models.DecimalField(
        max_digits=MAX_BUNDLE_DISCOUNT_DIGITS,
        decimal_places=MAX_BUNDLE_DISCOUNT_DECIMAL_PLACES,
        default=BUNDLE_DISCOUNT_DEFAULT,
    )
    start_date = models.DateTimeField(
        null=False,
        blank=False,
    )
    end_date = models.DateTimeField(
        null=False,
        blank=False,
    )
    active = models.BooleanField(
        default=True,
    )
    special_picture = models.URLField(
        null=False,
        blank=False,
    )

    def has_missing_products(self):
        current_count = self.products.count()
        return current_count < self.products_count

    def is_active(self):
        return self.active and self.start_date <= timezone.now() <= self.end_date and not self.has_missing_products()

    def get_bundle_price(self):
        total_price = sum(product.price for product in self.products.all())
        if self.is_active():
            if self.offer_type == 'percentage':
                total_price = total_price - total_price * (self.bundle_discount / 100)
            else:
                total_price = total_price - self.bundle_discount

        return round(total_price, 2)


class Recipe(models.Model):
    MAX_RECIPE_LENGTH = 1000

    ingredients = models.JSONField(
        null=False,
        blank=False,
    )
    recipe = models.TextField(
        max_length=MAX_RECIPE_LENGTH,
        null=False,
        blank=False,
    )
    product = models.OneToOneField(
        Product,
        on_delete=models.CASCADE,
        primary_key=True,
        related_name='product'
    )
    chef = models.ForeignKey(
        Cooker,
        on_delete=models.DO_NOTHING,
        related_name='chef',
        blank=True,
        null=True,
    )




