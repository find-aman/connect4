from django.urls import path
from .views import Game, PlayGame


urlpatterns = [
    path("game/", Game.as_view(), name="game"),
    path("play-game/", PlayGame.as_view(), name="play-game"),
]
