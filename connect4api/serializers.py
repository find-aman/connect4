from rest_framework import serializers
from .models import MovesData


class Moves(serializers.ModelSerializer):
    class Meta:
        model = MovesData
        fields = ["key", "move", "column", "player", "state", "winstatus"]
