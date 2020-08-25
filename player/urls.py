from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from player.views import home, new_invitation, accept_invitation, SignUpView

urlpatterns = [
  path('home', home, name="player_home"),

  # Create New Invite
  path(
    'new_invitation/',
    new_invitation,
    name='player_new_invitation'
  ),

  # Accept Invite
  path(
    'accept_invitation/<int:id>',
    accept_invitation,
    name='player_accept_invitation'
  ),

  # Login
  path(
      'login/',
      LoginView.as_view(template_name='player/login_form.html'),
      name='player_login'
  ),

  # Logout
  path(
      'logout/',
      LogoutView.as_view(),
      name='player_logout'
  ),

  # Sign up
  path(
    'signup',
    SignUpView.as_view(),
    name = 'player_signup'
  )
]