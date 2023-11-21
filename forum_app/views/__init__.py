from .main_views.index import MainView
from .main_views.forum import ForumListView
from .main_views.register import RegisterView
from .main_views.login import LoginUserView, logout_user
from .main_views.profile import ProfileView
from .main_views.edit_comment import UpdateComment, delete_comment
from .main_views.posts import PostListView
from .main_views.post_detail import PostDetailView, toggle_post_like, toggle_comment_like
from .main_views.add_post import CreatePost
from .main_views.edit_post import EditPost, delete_post
from .main_views.add_category import ajax_create_category, ajax_del_category
from .main_views.history import ProfileHistoryView
from .main_views.settings import ProfileSettingsView
from .main_views.profile_users_posts import ProfilePostListView, ProfileDraftsListView



