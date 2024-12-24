from django.contrib import auth, admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import profile

urlpatterns = [
    path('accounts/profile/', profile, name='profile'),
    path('admin/', admin.site.urls),
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='accounts')),
    path('accounts/password_reset/done/', auth.views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/done/', auth.views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('', include('reviews.urls')),
    path('filter_demo/', include('filter_demo.urls')),
    path('book_management/', include('book_management.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)