from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rada.modules.exceptions import raise_serializer_error_msg
from rada.modules.permissions import IsAdmin
from rada.modules.utils import api_response, get_incoming_request_checks, incoming_request_checks
from blog.models import Blog
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView

from blog.serializers import BlogSerializer, BlogListSerializer

# Create your views here.
class BlogView(ModelViewSet):
    permission_classes = [IsAuthenticated & IsAdmin]
    # permission_classes = [IsAuthenticated & (IsAdminUser)]

    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()
   
    def list(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        # queryset = Cart.objects.filter(owner=self.request.user).first()
        queryset : list[Blog] = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = BlogListSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = BlogListSerializer(queryset, many=True)
        
        
        return Response(
                api_response(
                    message="Categories retreived successfully",
                    status=True,
                    data=serializer.data,
                )
            )
        
    def create(self, request, *args, **kwargs):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(
                api_response(
                    message="Blog added successfully",
                    status=True,
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
                headers=headers
            )
        
    def retrieve(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(
                api_response(
                    message="Blog retreived successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def update(self, request, *args, **kwargs):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        # print(instance)
        serializer = self.serializer_class(instance, data=data, partial=partial)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        self.perform_update(serializer)

        return Response(
                api_response(
                    message="Blog updated successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def destroy(self, request, *args, **kwargs):
        get_incoming_request_checks(request)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            api_response( message="Blog deleted successfully", status=True),
            status=status.HTTP_204_NO_CONTENT
        )

class HomeBlog(APIView):
    serializer_class = BlogSerializer
    # queryset = Blog.objects.all()[0:5]
    
    def get(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)

        queryset = Blog.objects.all()[0:5]
        serializer = self.serializer_class(queryset, many=True)
        
        return Response(
                api_response(
                    message="Blogs retrieved successfully",
                    status=True,
                    data=serializer.data,
                )
            )