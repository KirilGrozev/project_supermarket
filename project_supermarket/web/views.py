from django.contrib.auth import login, get_user_model, authenticate, logout
from django.contrib.auth.mixins import LoginRequiredMixin, AccessMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DetailView, DeleteView

from project_supermarket.web.forms import RegisterUserForm, ProductEditForm, ProductDeleteForm, ProductCreateForm, \
    RecipeCreateForm, RecipeEditForm, RecipeDeleteForm, LoginUserForm, EditProfileForm
from project_supermarket.web.models import Product, Recipe, SpecialOffers, Cooker

UserModel = get_user_model()


class StaffOnlyMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Exception("You don't have the authorities to enter this page!")
        return super().dispatch(request, *args, **kwargs)


class Home(ListView):
    template_name = 'home.html'
    queryset = SpecialOffers.objects.all().\
        prefetch_related('products')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_active = [True for o in SpecialOffers.objects.all() if o.is_active()]
        are_all_active = True
        if all_active == [] or all(all_active) is False:
            are_all_active = False

        context['are_all_active'] = are_all_active

        return context


class Dashboard(ListView):
    template_name = 'dashboard.html'
    model = Product

    slug_url_kwarg = 'product_slug'


class Register(CreateView):
    model = UserModel
    template_name = 'register.html'
    form_class = RegisterUserForm
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        result = super().form_valid(form)
        user = authenticate(
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password1']
        )
        login(self.request, user)

        return result


class Login(LoginView):
    model = UserModel
    template_name = 'login.html'
    form_class = LoginUserForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('dashboard')


class Logout(LoginRequiredMixin, LogoutView):
    def get(self, request):
        logout(request)
        return redirect('home')


class EditProfile(LoginRequiredMixin, UpdateView):
    template_name = 'edit_profile.html'
    model = UserModel
    form_class = EditProfileForm
    success_url = reverse_lazy('dashboard')


class DeleteProfile(LoginRequiredMixin, DeleteView):
    template_name = 'delete_profile.html'
    model = UserModel
    success_url = reverse_lazy('home')


class Basket(TemplateView):
    template_name = 'basket.html'


class AboutUs(ListView):
    template_name = 'about_us.html'
    model = Cooker


class CreateProduct(StaffOnlyMixin, LoginRequiredMixin, CreateView):
    template_name = 'create_product.html'
    queryset = Product.objects.all(). \
        prefetch_related('cooker')

    form_class = ProductCreateForm

    def get_success_url(self):
        return reverse('product details', kwargs={
            'product_slug': self.object.slug,
        })


class ProductDetails(LoginRequiredMixin, DetailView):
    template_name = 'product_details.html'
    queryset = Product.objects.all().\
        prefetch_related('cooker')

    slug_url_kwarg = 'product_slug'


class EditProduct(StaffOnlyMixin, LoginRequiredMixin, UpdateView):
    template_name = 'edit_product.html'
    queryset = Product.objects.all(). \
        prefetch_related('cooker')
    form_class = ProductEditForm
    slug_url_kwarg = 'product_slug'

    def get_success_url(self):
        return reverse('product details', kwargs={
            'product_slug': self.object.slug
        })


class DeleteProduct(StaffOnlyMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delete_product.html'
    model = Product
    form_class = ProductDeleteForm
    success_url = reverse_lazy('dashboard')
    slug_url_kwarg = 'product_slug'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs


class Recipes(LoginRequiredMixin, ListView):
    template_name = 'recipes.html'
    model = Recipe


class CreateRecipe(StaffOnlyMixin, LoginRequiredMixin, CreateView):
    template_name = 'create_recipe.html'
    queryset = Recipe.objects.all(). \
        prefetch_related('product'). \
        prefetch_related('chef')

    form_class = RecipeCreateForm

    def get_success_url(self):
        return reverse('recipe details', kwargs={
            'pk': self.object.pk,
        })


class RecipeDetails(LoginRequiredMixin, DetailView):
    template_name = 'recipe_details.html'
    queryset = Recipe.objects.all().\
        prefetch_related('product').\
        prefetch_related('chef')


class EditRecipe(StaffOnlyMixin, LoginRequiredMixin, UpdateView):
    template_name = 'edit_recipe.html'
    queryset = Recipe.objects.all(). \
        prefetch_related('product'). \
        prefetch_related('chef')

    form_class = RecipeEditForm

    def get_success_url(self):
        return reverse('recipe details', kwargs={
            'pk': self.object.pk,
        })


class DeleteRecipe(StaffOnlyMixin, LoginRequiredMixin, DeleteView):
    template_name = 'delete_recipe.html'
    model = Recipe
    form_class = RecipeDeleteForm
    success_url = reverse_lazy('recipes')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['instance'] = self.object
        return kwargs
