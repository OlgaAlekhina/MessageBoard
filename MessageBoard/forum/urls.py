from django.urls import path
from .views import PostList, PostDetail, PostCreateView, PostUpdateView, PostDeleteView, ReplyCreateView, ThanksView, MessagesView, ReplyDeleteView, CategoryView, accept_reply

urlpatterns = [
    path('', PostList.as_view(), name='main'),
    path('<int:pk>', PostDetail.as_view(), name='post_detail'),
    path('add', PostCreateView.as_view(), name='post_create'),
    path('<int:pk>/edit', PostUpdateView.as_view(), name='post_edit'),
    path('<int:pk>/delete', PostDeleteView.as_view(), name='post_delete'),
    path('<int:pk>/reply', ReplyCreateView.as_view(), name='reply'),
    path('thanks', ThanksView.as_view(), name='thanks'),
    path('messages/', MessagesView.as_view(), name='messages'),
    path('messages/<int:pk>/delete/', ReplyDeleteView.as_view(), name='reply_delete'),
    path('messages/<int:pk>/accept/', accept_reply, name='reply_accept'),
    path('category/<int:cats>/', CategoryView.as_view(), name='post-category'),

    ]