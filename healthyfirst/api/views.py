from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from healthyfirst.api.serializers import PersonSerializer
from healthyfirst.api.models import Person
from healthyfirst.api.permissions import PersonPermission


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
        else:
            return [IsAuthenticated(), PersonPermission()]
