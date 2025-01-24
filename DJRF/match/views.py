from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Match, Over, Ball
from .serializers import MatchSerializer, BallSerializer


class MatchViewSet(ModelViewSet):
    queryset = Match.objects.all()
    serializer_class = MatchSerializer

    @action(detail=True, methods=["POST"])
    def add_ball(self, request, pk=None):
        match = self.get_object()
        over_number = match.overs_completed + 1
        over, _ = Over.objects.get_or_create(match=match, over_number=over_number)

        ball_data = request.data
        ball_data["over"] = over.id

        ball_serializer = BallSerializer(data=ball_data)
        if ball_serializer.is_valid():
            ball = ball_serializer.save()
            match.current_score += ball.runs + ball.extras
            if ball.is_wicket:
                match.wickets_fallen += 1
            match.save()
            return Response(
                {"message": "Ball added successfully", "data": ball_serializer.data}
            )
        return Response(ball_serializer.errors, status=400)

    @action(detail=True, methods=["POST"])
    def end_over(self, request, pk=None):
        match = self.get_object()
        match.overs_completed += 1
        match.save()
        return Response(
            {
                "message": "Over ended successfully",
                "overs_completed": match.overs_completed,
            }
        )

    @action(detail=True, methods=["GET"])
    def match_statistics(self, request, pk=None):
        match = self.get_object()
        serializer = self.get_serializer(match)
        return Response(serializer.data)
