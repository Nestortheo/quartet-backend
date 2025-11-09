from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import ConcertViewSet, VenueViewSet, CompositionViewSet

router = DefaultRouter()
router.register(r'concerts', ConcertViewSet)
router.register(r'venues', VenueViewSet)
router.register(r'compositions', CompositionViewSet)

urlpatterns = [

    path('', include(router.urls)),
]