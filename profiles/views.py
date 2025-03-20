from django.contrib.auth.models import User
from django.views.generic import DetailView,UpdateView
from .models import Profile
from .forms import ProfileUpdateForm

# # Create your views here.


class ProfileDetailView(DetailView):
    http_method_names = ['get']
    model = User
    template_name = 'profiles/detail.html'
    context_object_name = 'profile_user'  # Rename to avoid confusion
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        profile_user = self.get_object()  # The user whose profile is being viewed
        context = super().get_context_data(**kwargs)
        context['profile_user'] = profile_user  # Add the profile user to the context
        context['current_user'] = self.request.user  # Add the currently logged-in user

        # Total posts and followers logic here (using profile_user)
        # ...

        return context
    
class ProfileUpdateView(UpdateView):
    http_method_names = ['get', 'post']
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'profiles/update.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)