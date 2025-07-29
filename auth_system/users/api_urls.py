from django.urls import path
from .views import RegisterView, LoginView, ProfileView, LogoutView, DeleteAccountView
from .mock_views import DocumentsView, ProjectsView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='api_register'),
    path('login/', LoginView.as_view(), name='api_login'),
    path('profile/', ProfileView.as_view(), name='api_profile'),
    path('logout/', LogoutView.as_view(), name='api_logout'),
    path('delete-account/', DeleteAccountView.as_view(), name='api_delete_account'),

    path('documents/', DocumentsView.as_view(), name='api_documents'),
    path('projects/', ProjectsView.as_view(), name='api_projects')
]