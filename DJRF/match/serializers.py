from django.shortcuts import render
from .models import Match,Over,Ball
from rest_framework import serializers

class BallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ball
        fields = "_all__"

class Overserializer(serializers.ModelSerializer):
    balls = BallSerializer(many=True,read_only=True)
    class Meta:
        model = Over
        fields = ['id','over_number','balls','match']

class MatchSerializer(serializer.ModelSerializer):
    overs = Overserializer(many=True,read_only=True)
    class Meta:
        model = Match
        fields = ['id','name','team1','team2','current_score','wickets_fallen','overs_completed','overs']
        