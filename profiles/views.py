from django.contrib.auth.models import User
from django.views.generic import DetailView,UpdateView
from .models import Profile
from .forms import ProfileUpdateForm
from django.http import JsonResponse,HttpResponseBadRequest
from django.views import View
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User

from followers.models import Followers

# # Create your views here.


class ProfileDetailView(DetailView):
    http_method_names = ['get']
    model = User
    template_name = 'profiles/detail.html'
    context_object_name = 'profile_user'  
    slug_field = 'username'
    slug_url_kwarg = 'username'

    

    def get_context_data(self, **kwargs):
        profile_user = self.get_object()  # The user whose profile is being viewed
        context = super().get_context_data(**kwargs)
        context['profile_user'] = profile_user  # Add the profile user to the context
        context['current_user'] = self.request.user  # Add the currently logged-in user
        
        profile = Profile.objects.get(user=profile_user)
        context['profile'] = profile
        # Total posts and followers logic here (using profile_user)
        # ...
        context['total_posts'] = profile_user.posts.count()
        context['total_follower'] = Followers.objects.filter(followed_by=profile_user).count()

        # context['total_following'] = profile.following.count()

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

class FollowView(View):
        http_method_names = ['post']
        

       
        def post(self, request, *args, **kwargs):
            data = request.POST.dict()
            
            if "action" not in data or "username" not in data:
                return HttpResponseBadRequest("Missing Data")
            
            try:
                 other_user = User.objects.get(username=data['username'])
            except User.DoesNotExist:
                 return HttpResponseBadRequest("Missing Username")
            
            if data['action'] == 'follow':
                 #Follow
                 follower,created = Followers.objects.get_or_create(
                      followed_by=request.user,
                      following=other_user
                 )
            else:
                 #Unfollow
                try:
                    follower = Followers.objects.get(
                        followed_by=request.user,
                        following=other_user
                 )
                except Followers.DoesNotExist:
                     follower=None
                if follower:
                     follower.delete()
                

            return JsonResponse({
                  'success': True,
                  'wording': "Unfollow" if data['action']=="follow" else "Follow"
             })