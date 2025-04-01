from rest_framework import serializers
from rada.modules.exceptions import InvalidRequestException
from rada.modules.utils import api_response
from .models import Blog



class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = "__all__"

class BlogListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        # fields = "__all__"
        exclude = ['body']