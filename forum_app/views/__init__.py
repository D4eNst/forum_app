from .index import MainView
from .forum import ForumListView
from .post_detail import PostDetailView, toggle_comment_like, toggle_post_like
from .posts import PostListView
from .register import RegisterView
from .login import LoginUserView, logout_user
from .profile import ProfileView
from .edit_comment import UpdateComment, delete_comment
from .add_post import CreatePost
from .edit_post import EditPost, delete_post
from .add_category import ajax_create_category, ajax_del_category
from .history import ProfileHistoryView
from .settings import ProfileSettingsView
from .profile_users_posts import ProfilePostListView, ProfileDraftsListView



