from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from healthyfirst.api.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
        if self.action == 'create' or self.action == 'destroy':
            return [AllowAny()]
        else:
            return [IsAuthenticated()]

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk):
        queryset = User.objects.all()
        user = get_object_or_404(queryset, username=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def create(self, request):
        queryset = User.objects.all()
        new_user = queryset.create(
            username=request.data['username'],
        )
        new_user.set_password(request.data['password'])
        new_user.save()
        serializer = UserSerializer(new_user)
        return Response(serializer.data)

    def destroy(self, request, pk=None):
        if pk is not None:
            queryset = User.objects.all()
            user = get_object_or_404(queryset, username=pk)
            if user is not None:
                self.perform_destroy(user)
            return Response(status=status.HTTP_200_OK)

        return Response(status=status.HTTP_204_NO_CONTENT)


