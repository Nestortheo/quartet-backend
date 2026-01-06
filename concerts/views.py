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
    queryset = Concert.objects.all()  # just for router inference
    serializer_class = ConcertSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        qs = Concert.objects.all() if self.request.user.is_staff else Concert.objects.filter(is_public=True)
        return qs.order_by("date_start")

class VenueViewSet(viewsets.ModelViewSet):
    queryset = Venue.objects.all()
    serializer_class = VenueSerializer
    permission_classes = [IsAdminOrReadOnly]

class CompositionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Composition.objects.select_related('concert').all()
    serializer_class = CompositionSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['concert']          # /api/compositions/?concert=1
    search_fields = ['composer', 'title']   # /api/compositions/?search=Bartok
    ordering_fields = ['order', 'id']       # /api/compositions/?ordering=order
    ordering = ['order', 'id']
#EMAIL
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.conf import settings

@api_view(["POST"])
@permission_classes([AllowAny])
def contact(request):
    name = (request.data.get("name") or "").strip()
    email = (request.data.get("email") or "").strip()
    subject = (request.data.get("subject") or "").strip()
    message = (request.data.get("message") or "").strip()
    company = (request.data.get("company") or "").strip()

    if company:
        return Response({"ok": True})

    if not all([name, email, subject, message]):
        return Response({"detail": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

    full_subject = f"[Quartet Contact] {subject}"
    body = f"From: {name} <{email}>\n\n{message}"

    send_mail(
        subject=full_subject,
        message=body,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[getattr(settings, "CONTACT_RECEIVER_EMAIL", settings.DEFAULT_FROM_EMAIL)],
        fail_silently=False,
    )

    return Response({"ok": True})

