from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter

import forum_app.views as views

router = DefaultRouter()
router.register(r'posts', views.PostApiView, basename='api-post')
router.register(r'categories', views.CategoryApiView, basename='api-categories')
router.register(r'users', views.UserApiView, basename='api-users')
router.register(r'comments', views.CommentApiView, basename='api-comment')


urlpatterns = [
    path('', views.MainView.as_view(), name='main-page'),
    path('forum/', views.ForumListView.as_view(), name='forum'),

    path('post/create/', views.CreatePost.as_view(), name='create-post'),
    path('comment/delete/<slug:slug>/', views.delete_post, name='delete-post'),
    path('post/edit/<slug:slug>/', views.EditPost.as_view(), name='edit-post'),
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),

    path('category/<slug:slug>/', views.PostListView.as_view(), name='post_list'),
    path('ajax_create_category/', views.ajax_create_category, name='ajax-create-category'),
    path('ajax_del_category/', views.ajax_del_category, name='ajax-del-category'),

    path('singup/', views.RegisterView.as_view(), name='signup'),
    path('login/', views.LoginUserView.as_view(), name='login'),
    path('log-out/', views.logout_user, name='log-out'),

    path('toggle-comment-like/<int:comment_id>/', views.toggle_comment_like, name='toggle-comment-like'),
    path('toggle-post-like/<int:post_id>/', views.toggle_post_like, name='toggle-post-like'),

    path('history/<slug:username>/', views.ProfileHistoryView.as_view(), name='history'),
    path('settings/<slug:username>/', views.ProfileSettingsView.as_view(), name='settings'),
    path('profile/posts/<slug:username>/', views.ProfilePostListView.as_view(), name='users-posts'),
    path('profile/drafts/<slug:username>/', views.ProfileDraftsListView.as_view(), name='users-drafts'),
    path('profile/<slug:username>/', views.ProfileView.as_view(), name='profile'),


    path('comment/edit/<int:comment_id>/', views.UpdateComment.as_view(), name='edit-comment'),
    path('comment/delete/<int:comment_id>', views.delete_comment, name='delete-comment'),

    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
    path('api/v1/', include(router.urls)),
]
