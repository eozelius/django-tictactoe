from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator

GAME_STATUS_CHOICES = (
  ('F', 'First Player To Move'),
  ('S', 'Second Player To Move'),
  ('W', 'First Player Wins'),
  ('L', 'Second Player Wins'),
  ('D', 'Draw')
)

BOARD_SIZE = 3

class GamesQuerySet(models.QuerySet):
  def sorted_games_for_player(self, user):
    all_games = self.filter(Q(first_player = user) | Q(second_player = user))

    players_turn_games = all_games.filter(
      Q(Q(first_player = user) & Q(status = 'F')) |
      Q(Q(second_player = user) & Q(status = 'S'))
    )
    
    not_players_turn_games = all_games.filter(
      Q(Q(first_player = user) & Q(status = 'S')) |
      Q(Q(second_player = user) & Q(status = 'F'))
    )

    return {
      'my_turn': players_turn_games,
      'not_my_turn': not_players_turn_games
    }
  
  def players_turn_games(self, user):
    return self.filter(
      Q(first_player = user) & Q(status = 'F') |
      Q(second_player = user) & Q(status = 'S')
    )
  
  def games_for_user(self, user):
    return self.filter(
      Q(first_player = user) | Q(second_player = user)
    )

  def active(self):
    return self.filter(
      Q(status = 'F') | Q(status = 'S')
    )

class Game(models.Model):
  first_player = models.ForeignKey(User, related_name="games_first_player", on_delete=models.CASCADE)
  second_player = models.ForeignKey(User, related_name="games_second_player", on_delete=models.CASCADE)

  start_time = models.DateTimeField(auto_now_add=True)
  last_active = models.DateTimeField(auto_now=True)
  status = models.CharField(max_length=1, default='F', choices=GAME_STATUS_CHOICES)

  # override default Game.objects manager.
  objects = GamesQuerySet.as_manager()

  def get_absolute_url(self):
    return reverse('gameplay_detail', args=[self.id])

  def board (self):
    board = [[None for x in range(BOARD_SIZE)] for y in range(BOARD_SIZE)]
    for move in self.move_set.all():
      board[move.x][move.y] = move
    return board

  def is_users_move (self, user):
    return \
      (self.status == 'F' and self.first_player == user) \
      or \
      (self.status == 'S' and self.second_player == user)

  def new_move (self):
    """Returns a new move object with player, game and count preset"""
    if self.status not in 'FSD':
      raise ValueError('Game completed.')
    
    return Move(
      game = self,
      by_first_player = self.status == 'F'
    )

  def update_after_move(self, move):
    self.status = self._get_game_status_after_move(move)

  def _get_game_status_after_move (self, move):
    x, y = int(move.x), int(move.y)
    board = self.board()

    # Win condition: Horizontal
    if (board[x][0] == board[x][1] == board[x][2]):
      print('Horizontal Win')
      return 'W' if move.by_first_player else 'L'
    else:
      print('Horizontal FALSE')

    # Win condition: Vertical
    if (board[0][y] == board[1][y] == board[2][y]):
      print('Vertical Win')
      return 'W' if move.by_first_player else 'L'
    else:
      print('Vertical FALSE')

    # Win condition: Diagonal SW/NE
    if board[1][1] is not None:
      if (board[0][0] == board[1][1] == board[2][2]) and \
        board[0][0] is not None:
        print('Diagonal 1 win')
        return 'W' if move.by_first_player else 'L'
      else:
        print('Diagonal 1 false')
    
      print('board[0][2] => ', board[0][2])
      print('board[1][1] => ', board[1][1])
      print('board[2][0] => ', board[2][0])

      # Win condition: Diagonal NW/SE
      if (board[0][2] == board[1][1] == board[2][0]):
        print('Diagonal 2 win')
        return 'W' if move.by_first_player else 'L'
      else:
        print('Diagonal 2 false')
    else:
      print('Not Eligible for Diagonal win check')
    
    # if (board[x][0] == board[x][1] == board[x][2]) or \
    #    (board[0][y] == board[1][y] == board[2][y]) or \
    #    (board[0][0] == board[1][1] == board[2][2]) or \
    #    (board[0][2] == board[1][1] == board[2][0]):
    #   return 'W' if move.by_first_player else 'L'

    # Game is drawn
    if self.move_set.count() >= BOARD_SIZE ** 2:
      return 'D'
    
    # return first or second player status
    return 'S' if self.status == 'F' else 'F'
    

  def __str__(self):
    return "[id: {0}] {1} vs {2}; status: {3}".format(
      self.id,
      self.first_player,
      self.second_player,
      self.status
    )

class Move(models.Model):
  x = models.IntegerField(
    validators = [
      MinValueValidator(0),
      MaxValueValidator(BOARD_SIZE - 1)
    ]
  )
  y = models.IntegerField(
    validators = [
      MinValueValidator(0),
      MaxValueValidator(BOARD_SIZE - 1)
    ]
  )
  comment = models.CharField(max_length=300, blank=True)
  by_first_player = models.BooleanField(editable=False)
  game = models.ForeignKey(Game, on_delete=models.CASCADE, editable=False)

  def __eq__ (self, other):
    if other is None:
      print('Move().__eq__ other is None')
      return False
    return other.by_first_player == self.by_first_player

  # override save method
  def save(self, *args, **kwargs):
    super(Move, self).save(*args, **kwargs)
    self.game.update_after_move(self)
    self.game.save()