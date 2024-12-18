from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from django.forms import Select

from project_supermarket.web.models import Product, Recipe

UserModel = get_user_model()


class ReadOnlySelect(Select):
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs['disabled'] = 'disabled'
        rendered_select = super().render(name + '_display', value, attrs, renderer)
        hidden_input = f'<input type="hidden" name="{name}" value="{value}">'
        return rendered_select + hidden_input


class RegisterUserForm(UserCreationForm):
    user = None

    class Meta(UserCreationForm.Meta):
        model = UserModel
        fields = ('first_name', 'last_name', 'date_of_birth', 'email')

        label = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'date_of_birth': 'Date Of Birth',
        }

    widgets = {
        'first_name': forms.TextInput(attrs={'placeholder': 'Enter First Name'}),
        'last_name': forms.TextInput(attrs={'placeholder': 'Enter Last Name'}),
        'date_of_birth': forms.DateInput(attrs={'type': 'date', 'placeholder': 'Enter Date Of Birth'}),
        'email': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = None


class LoginUserForm(AuthenticationForm):
    class Meta:
        model = UserModel
        fields = '__all__'

        label = {
            'username': 'Email',
            'password': 'Password'
        }

    widgets = {
        'username': forms.EmailInput(attrs={'placeholder': 'Enter Email'}),
        'password': forms.TextInput(attrs={'placeholder': 'Enter Password'})
    }


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserModel
        fields = ('first_name', 'last_name', 'date_of_birth', 'email')

        label = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'email': 'Email',
            'date_of_birth': 'Date Of Birth',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['readonly'] = True


class ProductCreateForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('slug',)

        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter Name'}),
            'price': forms.NumberInput(attrs={'placeholder': 'Enter Price'}),
            'category': forms.Select(attrs={'placeholder': 'Choose Category'}),
            'description': forms.Textarea(attrs={'rows': 5, 'cols': 6, 'placeholder': 'Enter Description'}),
            'cooker': forms.Select(attrs={'placeholder': 'Choose Cooker'}),
            'picture': forms.URLInput(attrs={'placeholder': 'Upload picture'})
        }

        label = {
            'name': 'Name',
            'price': 'Price',
            'category': 'Category',
            'description': 'Description',
            'cooker': 'Cooker',
            'picture': 'Picture'
        }


class ProductEditForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('slug',)

        label = {
            'name': 'Name',
            'price': 'Price',
            'category': 'Category',
            'description': 'Description',
            'cooker': 'Cooker',
            'picture': 'Picture'
        }

        widgets = {
            'category': ReadOnlySelect(),
            'cooker': ReadOnlySelect()
        }


class ProductDeleteForm(forms.ModelForm):
    class Meta:
        model = Product
        exclude = ('slug',)

        label = {
            'name': 'Name',
            'price': 'Price',
            'category': 'Category',
            'description': 'Description',
            'cooker': 'Cooker',
            'picture': 'Picture'
        }

        widgets = {
            'category': ReadOnlySelect(),
            'cooker': ReadOnlySelect()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance


class RecipeCreateForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

        widgets = {
            'ingredients': forms.Textarea(attrs={'rows': 5, 'cols': 60, 'placeholder': 'Enter Ingredients'}),
            'recipe': forms.Textarea(attrs={'rows': 5, 'cols': 60, 'placeholder': 'Enter Recipe'}),
            'product': forms.Select(attrs={'placeholder': 'Enter Ingredients'}),
            'chef': forms.Select(attrs={'placeholder': 'Enter Ingredients'})
        }

        label = {
            'ingredients': 'Ingredients',
            'recipe': 'Recipe',
            'product': 'Product',
            'chef': 'Chef'
        }


class RecipeEditForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

        label = {
            'ingredients': 'Ingredients',
            'recipe': 'Recipe',
            'product': 'Product',
            'chef': 'Chef'
        }

        widgets = {
            'product': ReadOnlySelect(),
            'chef': ReadOnlySelect()
        }


class RecipeDeleteForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = '__all__'

        label = {
            'ingredients': 'Ingredients',
            'recipe': 'Recipe',
            'product': 'Product',
            'chef': 'Chef'
        }

        widgets = {
            'product': ReadOnlySelect(),
            'chef': ReadOnlySelect()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['readonly'] = True

    def save(self, commit=True):
        if commit:
            self.instance.delete()
        return self.instance
