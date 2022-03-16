import django_filters
from .models import Post


def user_posts(request):
    if request is None:
        return Post.objects.none()
    user = request.user
    return user.post_set.all().order_by('-post_time')


class MessageFilter(django_filters.FilterSet):
    reply_filter = django_filters.ModelChoiceFilter(queryset=user_posts, field_name='reply_post', label='По названию объявления')


