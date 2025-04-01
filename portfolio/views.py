from django.shortcuts import render
import csv
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from blog.serializers import BlogSerializer
from rada.modules.exceptions import raise_serializer_error_msg
from rada.modules.pagination import CustomPagination
from rada.modules.permissions import IsAdmin, IsReadOnly
from rada.modules.utils import api_response, get_incoming_request_checks, incoming_request_checks
from blog.models import Blog
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from portfolio.models import (Clients, Contact, Project, 
                                Service, SubServices, Team, Testimonial)
from portfolio.serializers import (AdminContactSerializer, ClientsSerializer, ContactSerializerIn,
                                    ListAdminContactSerializer, ProjectSerializer, ServiceOnlySerializer, ServiceSerializer, SubServiceSerializer,
                                    TeamSerializer, TestimonialSerializer)
from rest_framework.filters import SearchFilter
# Create your views here.


class HomeData(APIView):
    # service_serializer_class = ServiceOnlySerializer
    blog_serializer_class = BlogSerializer
    testimonial_serializer_class = TestimonialSerializer
    
    def get(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        blogs = Blog.objects.all()[0:5]
        blogs_serializer = self.blog_serializer_class(blogs, many=True)

        testimonial = Testimonial.objects.all()
        testimonial_serializer = self.testimonial_serializer_class(testimonial, many=True)
        
        return Response(
                api_response(
                    message="Blogs retrieved successfully",
                    status=True,
                    data={
                        "news": blogs_serializer.data,    
                        # "teams": team_serializer.data,    
                        "testimonials": testimonial_serializer.data,    
                    }
                )
            )
    
    

class AboutUsPageView(APIView):

    team_serializer_class = TeamSerializer
    # client_serializer_class = ClientsSerializer
    # queryset = Blog.objects.all()[0:5]
    
    def get(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)

        # clients = Clients.objects.all()
        team = Team.objects.all()
        
        
        team_serializer = self.team_serializer_class(team, many=True)
        # client_serializer = self.client_serializer_class(clients, many=True)
        
        return Response(
                api_response(
                    message="Blogs retrieved successfully",
                    status=True,
                    data={
                        # "clients": client_serializer.data,    
                        "teams": team_serializer.data,
                    }
                )
            )



class ServiceView(ModelViewSet):
    permission_classes = [IsAuthenticated & (IsAdmin)]
    # permission_classes = [IsAuthenticated & (IsAdminUser)]
    pagination_class = CustomPagination
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()
    
    
    def get_serializer_class(self):
        if self.request.method in ["PATCH", "POST", "PUT"]:
            return ServiceOnlySerializer
        return super().get_serializer_class()
    
    @property
    def get_viewSchema(self):
        return "Services"
    
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()
   
    def list(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        # queryset = Cart.objects.filter(owner=self.request.user).first()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
            return Response(
                api_response(
                    message=f"{self.get_viewSchema} retreived successfully",
                    status=True,
                    data=data.data,
                )
            )

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
                api_response(
                    message="Services retreived successfully",
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
                    message="Services added successfully",
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
                    message="Services retreived successfully",
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
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        self.perform_update(serializer)

        return Response(
                api_response(
                    message="Services updated successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def destroy(self, request, *args, **kwargs):
        get_incoming_request_checks(request)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            api_response( message="Services deleted successfully", status=True),
            status=status.HTTP_204_NO_CONTENT
        )

class SubServiceView(ModelViewSet):
    # permission_classes = [IsAuthenticated & (IsAdminUser)]
    permission_classes = [IsAuthenticated & (IsAdmin)]
    pagination_class = CustomPagination
    serializer_class = SubServiceSerializer
    queryset = SubServices.objects.all()
    
    @property
    def get_viewSchema(self):
        return "SubServices"
    
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()
   
    def list(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        # queryset = Cart.objects.filter(owner=self.request.user).first()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
            return Response(
                api_response(
                    message=f"{self.get_viewSchema} retreived successfully",
                    status=True,
                    data=data.data,
                )
            )

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
                api_response(
                    message="Services retreived successfully",
                    status=True,
                    data=serializer.data,
                )
            )
        
    def create(self, request, *args, **kwargs):
        status_, data = incoming_request_checks(request)
        self.request.path
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
                    message="Services added successfully",
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
                    message="Services retreived successfully",
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
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        self.perform_update(serializer)

        return Response(
                api_response(
                    message="Services updated successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def destroy(self, request, *args, **kwargs):
        get_incoming_request_checks(request)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            api_response( message="Services deleted successfully", status=True),
            status=status.HTTP_204_NO_CONTENT
        )

# Create your views here.

class TeamView(ModelViewSet):
    # permission_classes = [IsAuthenticated & (IsAdminUser)]
    permission_classes = [IsAuthenticated & (IsAdmin)]
    pagination_class = CustomPagination
    serializer_class = TeamSerializer
    queryset = Team.objects.all()
    filter_backends = [SearchFilter]
    search_fields = ["name",
                    "role",
                    "phone",
                    "email",
                    "address",
                    "educational_qualification"]

    
    @property
    def get_viewSchema(self):
        return "Teams"
    
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()
   
    def list(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        # queryset = Cart.objects.filter(owner=self.request.user).first()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
            return Response(
                api_response(
                    message=f"{self.get_viewSchema} retreived successfully",
                    status=True,
                    data=data.data,
                )
            )

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
                api_response(
                    message="Services retreived successfully",
                    status=True,
                    data=serializer.data,
                )
            )
        
    def create(self, request, *args, **kwargs):
        status_, data = incoming_request_checks(request)
        self.request.path
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
                    message="Teams added successfully",
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
                    message="Teams retreived successfully",
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
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        self.perform_update(serializer)

        return Response(
                api_response(
                    message="Teams updated successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def destroy(self, request, *args, **kwargs):
        get_incoming_request_checks(request)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            api_response( message="Teams deleted successfully", status=True),
            status=status.HTTP_204_NO_CONTENT
        )

# Create your views here.
class ProjectsView(ModelViewSet):
    # permission_classes = [IsAuthenticated & (IsAdminUser)]
    permission_classes = [IsAuthenticated & (IsAdmin)]
    pagination_class = CustomPagination
    serializer_class = ProjectSerializer
    queryset = Project.objects.all()
    viewSchema = "project"
    
    @property
    def get_viewSchema(self):
        return "Project"
    
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()
   
    def list(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        # queryset = Cart.objects.filter(owner=self.request.user).first()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
            return Response(
                api_response(
                    message=f"{self.get_viewSchema} retreived successfully",
                    status=True,
                    data=data.data,
                )
            )

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
                api_response(
                    message=f"{self.get_viewSchema} retreived successfully",
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
                    message=f"{self.get_viewSchema} added successfully",
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
                    message=f"{self.get_viewSchema} retreived successfully",
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
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        self.perform_update(serializer)

        return Response(
                api_response(
                    message=f"{self.get_viewSchema} updated successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def destroy(self, request, *args, **kwargs):
        get_incoming_request_checks(request)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            api_response( message=f"{self.get_viewSchema} deleted successfully", status=True),
            status=status.HTTP_204_NO_CONTENT
        )

# Create your views here.
class TestimonialView(ModelViewSet):
    # permission_classes = [IsAuthenticated & (IsAdminUser)]
    permission_classes = [IsAuthenticated & (IsAdmin)]
    pagination_class = CustomPagination
    serializer_class = TestimonialSerializer
    queryset = Testimonial.objects.all()
    
    @property
    def get_viewSchema(self):
        return "Testimony"
    
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()
   
    def list(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        # queryset = Cart.objects.filter(owner=self.request.user).first()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
            return Response(
                api_response(
                    message=f"{self.get_viewSchema} retreived successfully",
                    status=True,
                    data=data.data,
                )
            )

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
                api_response(
                    message=f"{self.get_viewSchema} retreived successfully",
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
                    message=f"{self.get_viewSchema} added successfully",
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
                    message=f"{self.get_viewSchema} retreived successfully",
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
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        self.perform_update(serializer)

        return Response(
                api_response(
                    message=f"{self.get_viewSchema} updated successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def destroy(self, request, *args, **kwargs):
        get_incoming_request_checks(request)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            api_response( message=f"{self.get_viewSchema} deleted successfully", status=True),
            status=status.HTTP_204_NO_CONTENT
        )
# Create your views here.
class ContactUsView(ModelViewSet):
    # permission_classes = [IsAuthenticated & (IsAdminUser)]
    permission_classes = [IsAuthenticated & (IsAdmin)]
    
    pagination_class = CustomPagination
    serializer_class = AdminContactSerializer
    queryset = Contact.objects.order_by("-created","isClosed").all()
    filter_backends = [SearchFilter]
    search_fields = ["fullname", "email", "phone", "message", "isClosed"]
    
    def get_serializer_class(self):
        if self.request.method == "POST":
            return ContactSerializerIn
        # if not self.kwargs.get(self.lookup_field, None) is None:
        #     return ListAdminContactSerializer
        return super().get_serializer_class()
    
    @property
    def get_viewSchema(self):
        return "Contactus"
    
    def get_queryset(self):
        start_date = self.request.GET.get('start_date', None)
        end_date = self.request.GET.get('end_date', None)
        status = self.request.GET.get('status', None)

        
        queryset = super().get_queryset()
        
        
        if start_date and end_date:
            queryset = queryset.filter(
                    created__date__range=(start_date, end_date),
                )
            return queryset
        if status in ["true", "false"]:
            filter_status = True if status == "true" else False 
            queryset = queryset.filter(isClosed=filter_status)
        return queryset.order_by("-created", "isClosed")
        
    def get_permissions(self):
        if self.request.method == "POST":
            return []
        return super().get_permissions()
   
    @swagger_auto_schema(
        manual_parameters=[
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="A query parameter",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="A query parameter",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'status',
                openapi.IN_QUERY,
                description="A query parameter",
                type=openapi.TYPE_BOOLEAN
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        # queryset = Cart.objects.filter(owner=self.request.user).first()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
            return Response(
                api_response(
                    message=f"{self.get_viewSchema} retreived successfully",
                    status=True,
                    data=data.data,
                )
            )

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
                api_response(
                    message=f"{self.get_viewSchema} retreived successfully",
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
                    message=f"Message sent successfully",
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
                    message=f"{self.get_viewSchema} retreived successfully",
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
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        self.perform_update(serializer)

        return Response(
                api_response(
                    message=f"{self.get_viewSchema} updated successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def destroy(self, request, *args, **kwargs):
        get_incoming_request_checks(request)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            api_response( message=f"{self.get_viewSchema} deleted successfully", status=True),
            status=status.HTTP_204_NO_CONTENT
        )

class SubmitContactUsView(CreateAPIView):
    serializer_class = ContactSerializerIn
    
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
                    message=f"Contactus created successfully",
                    status=True,
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
                headers=headers
            )
            
class ClientsView(ModelViewSet):
    # permission_classes = [IsAuthenticated & (IsAdminUser)]
    permission_classes = [IsAuthenticated & (IsAdmin)]
    pagination_class = CustomPagination
    serializer_class = ClientsSerializer
    queryset = Clients.objects.all()
    
    @property
    def get_viewSchema(self):
        return "Client"
    
    def get_permissions(self):
        if self.request.method == "GET":
            return []
        return super().get_permissions()
   
    def list(self, request, *args, **kwargs):
        status_, data = get_incoming_request_checks(request)
        # queryset = Cart.objects.filter(owner=self.request.user).first()
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            data = self.get_paginated_response(serializer.data)
            return Response(
                api_response(
                    message=f"{self.get_viewSchema} retreived successfully",
                    status=True,
                    data=data.data,
                )
            )

        serializer = self.get_serializer(queryset, many=True)
        
        return Response(
                api_response(
                    message=f"{self.get_viewSchema} retreived successfully",
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
                    message=f"{self.get_viewSchema} added successfully",
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
                    message=f"{self.get_viewSchema} retreived successfully",
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
        serializer = self.serializer_class(instance, data=request.data, partial=partial)
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        self.perform_update(serializer)

        return Response(
                api_response(
                    message=f"{self.get_viewSchema} updated successfully",
                    status=True,
                    data=serializer.data,
                )
            )
    
    def destroy(self, request, *args, **kwargs):
        get_incoming_request_checks(request)
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            api_response( message=f"{self.get_viewSchema} deleted successfully", status=True),
            status=status.HTTP_204_NO_CONTENT
        )


class ExportContactCSVView(APIView):
    # permission_classes = [IsAdminUser]  # Restrict access to admins
    permission_classes = [IsAuthenticated & (IsAdmin | IsReadOnly)]
    

    def get(self, request, *args, **kwargs):
        # Define response with CSV content type
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="contacts.csv"'

        statuses = {
            "true": True,
            "false": False,
        }
        mesage_status = request.GET.get('status')
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        
        if start_date and end_date:
            queryset = Contact.objects.filter(
                    created__date__range=(start_date, end_date)
                ).order_by("-created")
            
        else: 
            queryset = Contact.objects.order_by("-created")
        # Get the queryset
        if mesage_status in ["true", "false"]:
            queryset = queryset.filter(isClosed=statuses[mesage_status])
        
        if request.GET.get('page_size'):
            paginator = CustomPagination()
            paginator.page_size = request.GET.get('page_size', 10)  # Default 10 per page
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = ListAdminContactSerializer(result_page, many=True)
            # Serialize data using the DRF serializer
        else:
            serializer = ListAdminContactSerializer(queryset, many=True)
            
        data = serializer.data

        if not data:
            return Response(
                api_response(message="No contacts found to export",
                             status=False,
                             data={}
                         )
            )

        # Create a CSV writer
        writer = csv.writer(response)

        # Write header row dynamically from serializer fields
        if data:
            writer.writerow(data[0].keys())

        # Write data rows
        for item in data:
            writer.writerow(item.values())

        return response
