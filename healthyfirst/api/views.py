from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from healthyfirst.api.serializers import PersonSerializer
from healthyfirst.api.models import Person
from healthyfirst.api.permissions import IsManager


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = PersonSerializer
    authentication_classes = [JWTAuthentication]
    queryset = Person.objects.all()
    lookup_field = 'username'

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        elif self.action == 'destroy' or self.action == 'list':
            return [IsAuthenticated(), IsManager()]
        else:
            return [IsAuthenticated()]

    def retrieve(self, request, username):
        if request.user.username != username:
            raise PermissionError("You can't ger other's information!")
        user = get_object_or_404(self.queryset, username=username)
        serializer = PersonSerializer(user)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.role == Person.MANAGER:
            raise PermissionError("Cannot delete manager user!")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
