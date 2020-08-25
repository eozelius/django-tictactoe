from django.urls import path

from gameplay.views import game_detail, make_move, AllGamesView

urlpatterns = [
  # GET all games
  path(
    '',
    AllGamesView.as_view(),
    name='all_games'
  ),
  
  # GET a game
  path(
    'detail/<int:id>',
    game_detail,
    name='gameplay_detail'
  ),

  # POST make a move
  path(
    'make_move/<int:id>',
    make_move,
    name='gameplay_make_move'
  )
]