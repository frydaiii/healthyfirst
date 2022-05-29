from rest_framework import viewsets
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from healthyfirst.api.serializers import PersonSerializer
from healthyfirst.api.models import Person
from healthyfirst.api.permissions import IsManager, ViewOwnResource


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
        elif self.action == 'retrieve':
            return [IsAuthenticated(), ViewOwnResource()]
        elif self.action == 'destroy' or self.action == 'list':
            return [IsAuthenticated(), IsManager()]
        else:
            return [IsAuthenticated()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.role == Person.MANAGER:
            raise PermissionError("Cannot delete manager user!")
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # check permission
        if request.user.role == Person.MANAGER:
            if instance.username != request.user.username:
                raise PermissionError("You cannot modify other manager!")
            else:
                pass
        if request.user.role == Person.STAFF:
            if request.user.username != instance.username:
                raise PermissionError("You cannot modify other staff!")
            else:
                pass

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)