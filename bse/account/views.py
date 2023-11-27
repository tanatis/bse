from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import Http404
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model, login
from django.contrib.auth import views as auth_views
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic as views
from typing import Protocol

from bse.account.forms import UserRegisterForm
from bse.account.models import Profile
from bse.utils.tokens import account_activation_token

UserModel = get_user_model()


def index(request):
    return render(request, 'index.html')


def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)

        messages.success(request, f"Thank you for your email confirmation. You are now logged in as {user.username}. \n Please update your profile-pictures.")
        return redirect('index')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('user_login')


def activate_email(request, user, to_email):
    mail_subject = 'Activate your account'
    message = render_to_string('account/activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.warning(request,
                         f"Dear {user}, please activate your account by clicking the link we've just sent you to {to_email}")
    else:
        messages.error(request, f"Problem sending mail to {to_email}")


class UserRegisterView(views.CreateView):
    model = UserModel
    template_name = 'account/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('user_login')

    def form_valid(self, form):
        response = super().form_valid(form)
        self.object.is_active = False
        self.object.save()
        Profile.objects.create(user=self.object)  # Create Profile for the user
        activate_email(self.request, self.object, form.cleaned_data.get('email'))
        # login(self.request, self.object)  # Automatically login the new registered user
        return response

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(request, 'You already have an account. No need to register again.')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class UserLoginView(auth_views.LoginView):
    template_name = 'account/login.html'

    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            messages.error(request, 'You are already logged in!')
            return redirect('index')
        return super().dispatch(request, *args, **kwargs)


class UserLogoutView(auth_views.LogoutView):
    pass


class UserListView(views.ListView):
    model = UserModel
    template_name = 'account/accounts.html'


class ProfileDetailsView(LoginRequiredMixin, views.DetailView):
    login_url = 'user_login'
    model = Profile
    template_name = 'account/profile-details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['pk'] = self.object.pk

        return context


class ProfileEditView(views.UpdateView):
    model = Profile
    template_name = 'account/profile-edit.html'
    fields = ['first_name', 'last_name', 'city', 'profile_picture']

    def get_success_url(self):
        return reverse_lazy('profile_details', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'You must be logged in to edit profile!')
            return redirect('user_login')
        profile = self.get_object()
        if self.request.user != profile.user:
            messages.error(request, 'You can only edit your own profile')
            return redirect('profile_edit', pk=request.user.pk)
        return super().dispatch(request, *args, **kwargs)


class ProfileDeleteView(UserPassesTestMixin, LoginRequiredMixin, views.DeleteView):
    login_url = 'user_login'
    success_url = reverse_lazy('index')
    template_name = 'account/profile-delete.html'
    model = UserModel

    def test_func(self):
        return self.get_object().pk == self.request.user.pk or self.request.user.is_superuser

    def handle_no_permission(self):
        raise Http404()
    