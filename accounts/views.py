from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.db.transaction import atomic
from django.forms import CharField, Textarea, DateField, ModelForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView

from accounts.models import Profile


class SubmittableLoginView(LoginView):
    template_name = 'form.html'


class SubmittablePasswordChangeView(PasswordChangeView):
    template_name = 'form.html'
    success_url = reverse_lazy('home')


class SignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']
        #fields = '__all__'

    birth_date = DateField()
    biography = CharField(label='Tell us your story with movies', widget=Textarea, min_length=40)

    @atomic
    def save(self, commit=True):
        self.instance.is_active = True
        result = super().save(commit)
        birth_date = self.cleaned_data['birth_date']
        biography = self.cleaned_data['biography']
        profile = Profile(birth_date=birth_date, biography=biography, user=result)
        if commit:
            profile.save()
        return result


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'


class SignUpView(CreateView):
    form_class = SignUpForm
    template_name = 'signup.html'
    success_url = reverse_lazy('home')


# List of profiles
class ProfilesListView(LoginRequiredMixin, ListView):
    template_name = 'profiles.html'
    model = Profile
    context_object_name = 'profiles'


# Profile view
class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profile.html'
    context_object_name = 'profile'


# TODO: Profile Create ?


# Profile update
class ProfileUpdateView(UserPassesTestMixin, UpdateView):
    template_name = 'form.html'
    model = Profile
    form_class = ProfileForm
    success_url = reverse_lazy('profiles')

    def test_func(self):
        if self.request.user.is_staff:
            return True
        try:
            profile = Profile.objects.get(id=self.kwargs['pk'])
            return self.request.user == profile.user
        except:
            return False


# Profile delete
class ProfileDeleteView(UserPassesTestMixin, DeleteView):
    template_name = 'profile_confirm_delete.html'
    model = Profile
    success_url = reverse_lazy('profiles')

    def test_func(self):
        if self.request.user.is_staff:
            return True
        try:
            profile = Profile.objects.get(id=self.kwargs['pk'])
            return self.request.user == profile.user
        except:
            return False
