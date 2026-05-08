from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Actor, Director

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

UserModel = get_user_model()

GENRE_CHOICES = [
    ("Action", "Action"),
    ("Adventure", "Adventure"),
    ("Animation", "Animation"),
    ("Comedy", "Comedy"),
    ("Crime", "Crime"),
    ("Documentary", "Documentary"),
    ("Drama", "Drama"),
    ("Family", "Family"),
    ("Fantasy", "Fantasy"),
    ("Horror", "Horror"),
    ("Mystery", "Mystery"),
    ("Romance", "Romance"),
    ("Sci-Fi", "Sci-Fi"),
    ("Thriller", "Thriller"),
    ("War", "War"),
]


class AdminUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False, initial=True)

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if UserModel.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    class Meta:
        model = UserModel
        fields = [
            "username",
            "email",
            "password1",
            "password2",
            "is_staff",
            "is_superuser",
            "is_active",
        ]


class AdminUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=False, widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if UserModel.objects.filter(email__iexact=email).exclude(
            pk=self.instance.pk
        ).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 or password2:
            if password1 != password2:
                self.add_error("password2", "Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data.get("password1")
        if password:
            user.set_password(password)
        if commit:
            user.save()
        return user

    class Meta:
        model = UserModel
        fields = [
            "username",
            "email",
            "is_staff",
            "is_superuser",
            "is_active",
        ]


class AdminMovieForm(forms.Form):
    title = forms.CharField(max_length=200)
    description = forms.CharField(required=False)
    release_date = forms.DateField(required=False)
    duration = forms.IntegerField(required=False, min_value=1)
    poster_url = forms.URLField(required=False)
    genre = forms.ChoiceField(
        choices=[("", "Select genre")] + GENRE_CHOICES,
        required=False,
    )
    director = forms.ModelChoiceField(
        queryset=Director.objects.order_by("last_name", "first_name"),
    )
    actors = forms.ModelMultipleChoiceField(
        queryset=Actor.objects.order_by("last_name", "first_name"),
        required=False,
    )


class AdminDirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ["first_name", "last_name", "birth_date"]


class AdminActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ["first_name", "last_name", "birth_date"]