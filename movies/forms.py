from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Actor, Director, Movie, GENRE_CHOICES


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


class AdminUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    is_staff = forms.BooleanField(required=False)
    is_superuser = forms.BooleanField(required=False)
    is_active = forms.BooleanField(required=False, initial=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ['username', 'email', 'password1', 'password2']:
            self.fields[name].widget.attrs['class'] = 'form-control'
        for name in ['is_staff', 'is_superuser', 'is_active']:
            self.fields[name].widget.attrs['class'] = 'form-check-input'

    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        if UserModel.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        return email

    class Meta:
        model = UserModel
        fields = ["username", "email", "password1", "password2", "is_staff", "is_superuser", "is_active"]


class AdminUserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(required=False, widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name in ['username', 'email']:
            self.fields[name].widget.attrs['class'] = 'form-control'
        for name in ['is_staff', 'is_superuser', 'is_active']:
            self.fields[name].widget.attrs['class'] = 'form-check-input'

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
        fields = ["username", "email", "is_staff", "is_superuser", "is_active"]


class AdminMovieForm(forms.ModelForm):
    genre = forms.ChoiceField(
        choices=[("", "Select genre")] + GENRE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    director = forms.ModelChoiceField(
        queryset=Director.objects.order_by("last_name", "first_name"),
        widget=forms.Select(attrs={'class': 'form-select'}),
    )
    actors = forms.ModelMultipleChoiceField(
        queryset=Actor.objects.order_by("last_name", "first_name"),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
    )

    class Meta:
        model = Movie
        fields = ["title", "description", "release_date", "duration", "poster_url", "genre", "director", "actors"]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Movie title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Short description'}),
            'release_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'duration': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'placeholder': '120'}),
            'poster_url': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://example.com/poster.jpg'}),
        }

    def clean_title(self):
        return self.cleaned_data["title"].strip()

    def clean_description(self):
        val = self.cleaned_data.get("description") or ""
        return val.strip() or None

    def clean_poster_url(self):
        val = self.cleaned_data.get("poster_url") or ""
        return val.strip() or None


class AdminDirectorForm(forms.ModelForm):
    class Meta:
        model = Director
        fields = ["first_name", "last_name", "birth_date"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class AdminActorForm(forms.ModelForm):
    class Meta:
        model = Actor
        fields = ["first_name", "last_name", "birth_date"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'birth_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
