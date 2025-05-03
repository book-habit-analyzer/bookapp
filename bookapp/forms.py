from django import forms
from .models import Book, User
from django.core.exceptions import ValidationError

# -----------------------------
# Book Form
# -----------------------------
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'status']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user from view
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Book.objects.filter(title=title, user=self.user).exists():
            raise ValidationError("You have already added a book with this title.")
        return title

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user  # Assign user to book
        if commit:
            instance.save()
        return instance


# -----------------------------
# User Registration Form
# -----------------------------
class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_profile_public']

    def save(self, commit=True):
        user = super().save(commit=False)
        # Use set_password if using AbstractBaseUser; here we use simple hash placeholder
        user.password_hash = self.cleaned_data['password']
        if commit:
            user.save()
        return user
