from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category, Reply
from .filters import MessageFilter
from .forms import PostForm, ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class PostList(ListView):
    model = Post
    template_name = 'main.html'
    context_object_name = 'posts'
    ordering = ['-post_time']
    paginate_by = 10


class PostDetail(DetailView):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(reply_post=self.kwargs["pk"]).filter(reply_approved=True)
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    template_name = 'post_create_form.html'
    form_class = PostForm

    def get_initial(self):
        initial = super().get_initial()
        initial['post_author'] = self.request.user
        return initial


class PostUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'post_update_form.html'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


class ReplyCreateView(LoginRequiredMixin, CreateView):
    template_name = 'reply_create_form.html'
    form_class = ReplyForm
    success_url = reverse_lazy('thanks')

    def get_initial(self):
        initial = super().get_initial()
        reply_post = get_object_or_404(Post, id=self.kwargs['pk'])
        initial['reply_author'] = self.request.user
        initial['reply_post'] = reply_post
        return initial


class ReplyDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'reply_delete_form.html'
    queryset = Reply.objects.all()
    success_url = reverse_lazy('messages')


class ThanksView(TemplateView):
    template_name = 'thanks_for_reply.html'


class MessagesView(LoginRequiredMixin, ListView):
    model = Reply
    context_object_name = 'messages'
    template_name = 'messages.html'
    login_url = '/accounts/login/'

    def get_queryset(self):
        user = self.request.user
        return Reply.objects.filter(reply_post__post_author=user).order_by('-reply_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = MessageFilter(self.request.GET, request=self.request, queryset=self.get_queryset())
        return context


class CategoryView(ListView):
    context_object_name = 'category_posts'
    template_name = 'post_category.html'
    paginate_by = 10

    def get_queryset(self):
        self.category = get_object_or_404(Category, id=self.kwargs['cats'])
        return Post.objects.filter(post_category=self.category).order_by('-post_time')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


def accept_reply(request, pk):
    reply = Reply.objects.get(id=pk)
    reply.reply_approved = 'True'
    reply.save()
    return redirect('messages')



