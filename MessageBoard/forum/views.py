from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from .models import Post, Category, Reply
from .filters import MessageFilter
from .forms import PostForm, ReplyForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.models import User


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
        context = super(PostDetail, self).get_context_data(**kwargs)
        context['replies'] = Reply.objects.filter(reply_post=self.kwargs["pk"]).filter(reply_approved=True)
        if self.request.user in User.objects.all():
            context['is_author'] = Post.objects.filter(pk=self.kwargs["pk"], post_author=self.request.user).exists()
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


class PostDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'post_delete_form.html'
    queryset = Post.objects.all()
    success_url = '/main/'


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
    paginate_by = 10

    def get_filter(self):
        user = self.request.user
        queryset = Reply.objects.filter(reply_post__post_author=user).order_by('-reply_time')
        return MessageFilter(self.request.GET, request=self.request, queryset=queryset)

    def get_queryset(self):
        qs = self.get_filter().qs
        return qs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        filter = self.get_filter()
        context['filter'] = filter
        filter_params = ""
        for f_name in [str(k) for k in filter.filters]:
            if f_name in filter.data:
                filter_params += f"&{f_name}={filter.data[f_name]}"
        context['filter_params'] = filter_params
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



