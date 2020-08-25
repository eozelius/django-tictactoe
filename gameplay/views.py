from django.shortcuts import render
from gameplay.models import Game, Move
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic.list import ListView

@login_required
def game_detail (request, id):
  game = get_object_or_404(Game, pk=id)

  return render(
    request,
    'gameplay/game_detail.html',
    {
      'game': game,
      'by_first_player': game.first_player == request.user,
      'is_users_move': game.is_users_move(request.user)
    }
  )

@login_required
def make_move (request, id):
  game = get_object_or_404(Game, pk=id)
  
  if not game.is_users_move(request.user):
    raise PermissionDenied

  move = game.new_move()

  print('make_move() move =>', move)

  move.x = request.POST['row']
  move.y = request.POST['col']
  move.save()  
  return redirect('gameplay_detail', id)

class AllGamesView(ListView):
  model = Game  