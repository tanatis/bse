from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from bse.account.views import UserListView, UserRegisterView, UserLoginView, UserLogoutView, activate, \
    ProfileDetailsView, ProfileEditView, ProfileDeleteView

urlpatterns = [
    path('accounts/', UserListView.as_view(), name='accounts'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('profile/<int:pk>/', ProfileDetailsView.as_view(), name='profile_details'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='profile_edit'),
    path('profile/<int:pk>/delete/', ProfileDeleteView.as_view(), name='profile_delete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
