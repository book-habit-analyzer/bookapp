from django import forms
from .models import Book, User
from django.core.exceptions import ValidationError

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'status']

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Get user from kwargs
        super().__init__(*args, **kwargs)

    def clean_title(self):
        title = self.cleaned_data['title']
        if Book.objects.filter(title=title, user=self.user).exists():
            raise ValidationError("You have already added a book with this title.")
        return title

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.user  # Assign the user before saving
        if commit:
            instance.save()
        return instance


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'is_profile_public']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password_hash = self.cleaned_data['password']  # Simple store, not hashed
        if commit:
            user.save()
        return user
