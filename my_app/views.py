from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.db.models import Count
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Book, Comment
from .forms import CommentForm

class Home(LoginView):
    template_name = 'home.html'

@login_required
def my_books(request):
    user_books = Book.objects.filter(user=request.user).annotate(favorite_count=Count('favorited_by')).order_by('created_at')
    favorite_books = request.user.favorite_books.annotate(favorite_count=Count('favorited_by'))
    
    return render(request, 'my_books.html', {
        'books': user_books,
        'favorite_books': favorite_books,
    })

def book_index(request):
    category = request.GET.get('category')
    if category:
        books = Book.objects.filter(category=category).order_by('created_at')
    else:
        books = Book.objects.annotate(favorite_count=Count('favorited_by')).order_by('created_at')
    categories = Book.CATEGORY_CHOICES
    return render(request, 'books/index.html', {'books': books, 'categories': categories})

def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    comments = Comment.objects.filter(book=book)
    
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.book = book
            comment.save()
            return redirect('book-detail', book_id=book_id)
    else:
        form = CommentForm()

    return render(request, 'books/detail.html', {'book': book, 'comments': comments, 'form': form})

def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book-index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)

@login_required
def toggle_favorite(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.user in book.favorited_by.all():
        book.favorited_by.remove(request.user)
        favorited = False
    else:
        book.favorited_by.add(request.user)
        favorited = True
    return JsonResponse({'favorited': favorited})

@login_required
def update_background_color(request):
    if request.method == 'POST':
        color = request.POST.get('background_color')
        if color:
            request.user.profile.background_color = color
            request.user.profile.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'error'}, status=400)

class BookCreate(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'category', 'description', 'rating', 'cover_image']
    success_url = '/books/'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BookUpdate(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'category', 'description', 'rating', 'cover_image']
    success_url = '/books/'

class BookDelete(LoginRequiredMixin, DeleteView):
    model = Book
    success_url = '/books/'
