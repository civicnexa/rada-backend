from rest_framework import serializers
# from rada.modules.exceptions import InvalidRequestException
# from rada.modules.requestorigin import api_response
from .models import Clients, Contact, Project, Service, SubServices, Team, Testimonial


class SubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubServices
        fields = "__all__"

class ServiceSerializer(serializers.ModelSerializer):
    subservice = SubServiceSerializer(many=True)
    class Meta:
        model = Service
        fields = "__all__"

class ServiceOnlySerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = "__all__"

class TestimonialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Testimonial
        fields = "__all__"

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Clients
        fields = "__all__"
        # exclude = ['body']

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = "__all__"
        # exclude = ['body']

class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = "__all__"
        # exclude = ['body']

class ContactSerializerIn(serializers.ModelSerializer):
    class Meta:
        model = Contact
        # fields = "__all__"
        exclude = ['isClosed']

class AdminContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"

class ListAdminContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = "__all__"
        # exclude = ['message']