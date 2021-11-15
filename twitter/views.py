from django.views.generic import ListView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Post
from .forms import TweetForm
from User_Profile.models import Profile as ProfileModel
from django.shortcuts import render, redirect,get_object_or_404
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from taggit.models import Tag


# Create your views here.

class Home(LoginRequiredMixin, ListView):
    login_url = ''
    template_name = "twitter/home.html"
    raise_exception = True
    permission_denied_message = "You are not allowed here"
    context_object_name = "tweets"
    querySet = Post.objects.all()
    model = Post

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context['follow'] = ProfileModel.objects.all().exclude(user=self.request.user)
        context['posts'] = Post.objects.all()
        return context

class Tweet_Post(View):
    template_name = "twitter/Create_Tweet.html"
    model = ProfileModel
    form_class = TweetForm
    initial = {
        'content': 'World! is at your feet',
    }
    def get(self, request):
        form = self.form_class(initial = self.initial)
        return render(request, self.template_name, {'form': form})
    def post(self, request):

        form = self.form_class(request.POST)
        if form.is_valid():
            newpost = form.save(commit=False)
            newpost.author = self.request.user.profile
            newpost.slug = slugify(newpost.get_title())
            newpost.save()
            form.save_m2m()
            return redirect('twitter:home')
        return render(request, self.template_name, {'form':form})

def tagged(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    common_tags = Post.tags.most_common()[:4]
    posts = Post.objects.filter(tags=tag)
    context = {
        'tag': tag,
        'common_tags': common_tags,
        'posts': posts,
    }
    return render(request, 'twitter/home.html', context)