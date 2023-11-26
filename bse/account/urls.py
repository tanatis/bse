from django.urls import path

from bse.account.views import UserListView, UserRegisterView, UserLoginView, UserLogoutView, index, activate

urlpatterns = [
    path('', index, name='index'),
    path('accounts/', UserListView.as_view(), name='accounts'),
    path('login/', UserLoginView.as_view(), name='user_login'),
    path('logout/', UserLogoutView.as_view(), name='user_logout'),
    path('register/', UserRegisterView.as_view(), name='user_register'),
    path('activate/<uidb64>/<token>', activate, name='activate')
]
