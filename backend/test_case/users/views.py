from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User

from .serializers import UserSerializer


class UserViewSet(UserViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @action(detail=False, permission_classes=[IsAuthenticated])
    def me(self, request):
        user = User.objects.get(pk=request.user.id)
        serializer = self.get_serializer(user)
        return Response(serializer.data)
