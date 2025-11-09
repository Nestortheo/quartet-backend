from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets, filters
from .models import Concert, Venue, Composition
from .serializers import ConcertSerializer, VenueSerializer, CompositionSerializer
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, BasePermission, IsAuthenticated, \
    IsAuthenticatedOrReadOnly

from django_filters.rest_framework import DjangoFilterBackend


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit objects.
    Read-only for others.
    """

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_staff

class ConcertViewSet(viewsets.ModelViewSet):
    queryset = Concert.objects.all()
    serializer_class = ConcertSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class CompositionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Composition.objects.select_related('concert').all()
    serializer_class = CompositionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['concert']          # /api/compositions/?concert=1
    search_fields = ['composer', 'title']   # /api/compositions/?search=Bartok
    ordering_fields = ['order', 'id']       # /api/compositions/?ordering=order
    ordering = ['order', 'id']