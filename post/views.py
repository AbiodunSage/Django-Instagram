from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.views.generic import TemplateView,CreateView
from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import PostForm  # This is fine
from .models import Post, PostFile  # <--- Crucial: Import PostFile
from django.template.loader import render_to_string 



# ... (rest of your view code - no changes needed)

from .models import Post
from .forms import PostForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

# Create your views here.

class HomeView(LoginRequiredMixin,TemplateView):
    http_method_names = ['get']
    template_name = "home.html"

    def get_context_data(self, **kwargs):
        context=super().get_context_data(**kwargs)
        context['posts'] = Post.objects.all().order_by('-id')
        return context
@method_decorator(csrf_protect, name='dispatch')
class CreatePostView(CreateView):
    template_name = "create_post.html"
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        post = form.save()  # Save the Post (caption and author)

        # Handle the file upload and create PostFile instance
        uploaded_file = form.cleaned_data['file']
        post_file = PostFile(post=post, file=uploaded_file)
        post_file.save()

      
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                # Render the new post's HTML
                new_post_html = render_to_string('post_template.html', {'post': post}) # post_template.html is a template with only post content.
                return JsonResponse({'html': new_post_html}, status=200)  # Return HTML in JSON

                # messages.success(self.request, "Post created successfully!")
                # return super().form_valid(form)


    def form_invalid(self, form):
        if self.request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'error': 'Invalid form submission'}, status=400)
        return super().form_invalid(form)