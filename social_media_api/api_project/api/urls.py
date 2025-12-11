from django.urls import path
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .views import (
    BookList,
    BookDetail,
    register_view,
    logout_view,
)

from rest_framework.authtoken.views import obtain_auth_token


# ===========================
# API ROOT (Home of API)
# ===========================
@api_view(['GET'])
def api_root(request):
    return Response({
        "books": "/api/books/",
        "register": "/api/register/",
        "login": "/api/login/",
        "logout": "/api/logout/",
    })


# ===========================
# URL PATTERNS
# ===========================
urlpatterns = [
    path('', api_root, name='api-root'),

    # BOOKS
    path('books/', BookList.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetail.as_view(), name='book-detail'),

    # AUTH
    path('register/', register_view, name='api-register'),
    path('login/', obtain_auth_token, name='api-login'),
    path('logout/', logout_view, name='api-logout'),
]
