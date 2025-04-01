from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView
from . serializers import (TrackOwnerRegistrationSerializer,
                            EventPromoterRegistrationSerializer)
# Create your views here.

class ApplyforRacingLicense(CreateAPIView):
    # serializer_class = m
    
    def post(self, request):
        pass

class ApplyforTrackOwnerLicense(CreateAPIView):
    serializer_class = TrackOwnerRegistrationSerializer
    
    def post(self, request):
        pass

class ApplyforEventPromoterLicense(CreateAPIView):
    serializer_class = EventPromoterRegistrationSerializer
