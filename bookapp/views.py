from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from bookapp.models import Book
from bookapp.forms import BookForm, UserForm


@login_required
def new_book_form(request):
    """Render form for adding a new book."""
    return render(request, "bookForm.html", {"form": BookForm(user=request.user)})


@login_required
def my_list(request):
    """Display and manage books added by the logged-in user."""
    user_books = Book.objects.filter(user=request.user)
    labels = [book.title for book in user_books]
    data = [100 if book.status == "Completed" else 0 for book in user_books]  # Example progress logic

    if request.method == "POST":
        form = BookForm(request.POST, user=request.user)
        if form.is_valid():
            form.save()
            return redirect("my_list")
    else:
        form = BookForm(user=request.user)

    return render(request, "myList.html", {
        "labels": labels,
        "data": data,
        "form": form,
        "books": user_books
    })


@login_required
def delete_book(request, pk):
    """Delete a specific book owned by the current user."""
    book = get_object_or_404(Book, pk=pk, user=request.user)
    if request.method == "POST":
        book.delete()
        return redirect("my_list")

    return render(request, "confirm_delete.html", {"book": book})


def register(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("my_list")
    else:
        form = UserForm()
    return render(request, 'register.html', {'form': form})

def view_list(request, list_id):
    """View to display books in a specific list (could be by genre or category)."""
    books = Book.objects.filter(user=request.user, list_id=list_id)  # Assuming list_id is a field in Book
    return render(request, 'view_list.html', {'books': books})

def new_list(request):
    # Your logic for handling the 'new list' view
    return render(request, 'your_template.html')


def login_view(request):
    """Log in user and redirect to book list."""
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        # Manual authentication for custom user model
        from bookapp.models import User
        try:
            user = User.objects.get(username=username, password_hash=password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect("my_list")
        except User.DoesNotExist:
            messages.error(request, "Invalid login")
    
    return render(request, "login.html")


def logout_view(request):
    """Log out user."""
    logout(request)
    return redirect("login")

@login_required
def my_list(request):
    user_books = Book.objects.filter(user=request.user)
    form = BookForm(request.POST or None, user=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("myList")
    return render(request, "myList.html", {
        "books": user_books,
        "form": form
    })

