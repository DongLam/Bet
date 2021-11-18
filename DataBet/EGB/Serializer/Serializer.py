from rest_framework import serializers

from EGB.models import Match


class MatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Match
        fields = ('team1',
                  'team2',
                  'odds1',
                  'odds2')