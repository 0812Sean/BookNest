from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('my-books/', views.my_books, name='my-books'),
    path('books/', views.book_index, name='book-index'),
    path('books/<int:book_id>/', views.book_detail, name='book-detail'),
    path('books/create/', views.BookCreate.as_view(), name='book-create'),
    path('books/<int:pk>/edit/', views.BookUpdate.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', views.BookDelete.as_view(), name='book-delete'),
    path('signup/', views.signup, name='signup'),
    path('books/<int:book_id>/toggle_favorite/', views.toggle_favorite, name='toggle-favorite'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)