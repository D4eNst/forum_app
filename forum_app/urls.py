from django.urls import path
from .views import MainView, ForumListView, PostDetailView, PostListView, \
    RegisterView, LoginUserView, logout_user, ProfileView, ProfileSettingsView, ProfileHistoryView, \
    toggle_comment_like, toggle_post_like, UpdateComment, delete_comment, \
    CreatePost, EditPost, delete_post, ajax_create_category, ajax_del_category,\
    ProfilePostListView, ProfileDraftsListView

urlpatterns = [
    path('', MainView.as_view(), name='main-page'),
    path('forum/', ForumListView.as_view(), name='forum'),

    path('post/create/', CreatePost.as_view(), name='create-post'),
    path('comment/delete/<slug:slug>/', delete_post, name='delete-post'),
    path('post/edit/<slug:slug>/', EditPost.as_view(), name='edit-post'),
    path('post/<slug:slug>/', PostDetailView.as_view(), name='post_detail'),

    path('category/<slug:slug>/', PostListView.as_view(), name='post_list'),
    path('ajax_create_category/', ajax_create_category, name='ajax-create-category'),
    path('ajax_del_category/', ajax_del_category, name='ajax-del-category'),

    path('singup/', RegisterView.as_view(), name='signup'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('log-out/', logout_user, name='log-out'),

    path('toggle-comment-like/<int:comment_id>/', toggle_comment_like, name='toggle-comment-like'),
    path('toggle-post-like/<int:post_id>/', toggle_post_like, name='toggle-post-like'),

    path('history/<slug:username>/', ProfileHistoryView.as_view(), name='history'),
    path('settings/<slug:username>/', ProfileSettingsView.as_view(), name='settings'),
    path('profile/posts/<slug:username>/', ProfilePostListView.as_view(), name='users-posts'),
    path('profile/drafts/<slug:username>/', ProfileDraftsListView.as_view(), name='users-drafts'),
    path('profile/<slug:username>/', ProfileView.as_view(), name='profile'),


    path('comment/edit/<int:comment_id>/', UpdateComment.as_view(), name='edit-comment'),
    path('comment/delete/<int:comment_id>', delete_comment, name='delete-comment'),

]
