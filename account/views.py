from django.contrib.auth.models import User
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from rest_framework import generics
from django.contrib.auth.password_validation import validate_password
from rada.modules.exceptions import raise_serializer_error_msg
from rada.modules.pagination import CustomPagination
from rada.modules.permissions import IsAgentAdmin, IsAdmin, IsReadOnly
from .serializers import SubscribersSerializer, UserSerializerIn, UserSerializerOut, LoginSerializerIn
from rada.modules.utils import (
    incoming_request_checks,
    api_response,
    get_incoming_request_checks,
    sendEmail
)
from django.utils import timezone

from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
import csv
import threading
from .models import Subscriber, UserOtp

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema


class SubScribeView(APIView):
    def post(self, request):
        pass
    
@csrf_exempt
@require_http_methods(["POST"])
def subscribe(request):
    try:
        data = json.loads(request.body)
        email = data.get("email")
        name = data.get("name")

        if not email or not name:
            return JsonResponse({"error": "Email and name are required"}, status=400)

        # Check if subscriber already exists
        subscriber, created = Subscriber.objects.get_or_create(
            email=email, defaults={"name": name}
        )

        if not created:
            return JsonResponse({"error": "Email already subscribed"}, status=400)

        return JsonResponse(
            {
                "message": "Successfully subscribed",
                "subscriber": {
                    "email": subscriber.email,
                    "name": subscriber.name,
                    "subscribed_at": subscriber.subscribed_at,
                },
            },
            status=201,
        )

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON data"}, status=400)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=500)



class ExportSubscribersCSVView(APIView):
    permission_classes = [IsAuthenticated & (IsAdmin | IsAgentAdmin | IsReadOnly)]
    
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
        ]
    )
    def get(self, request):
        return self.export_subscribers_csv(request)
    # @require_http_methods(["GET"])
    
    def export_subscribers_csv(self, request):
        # Check if user is authenticated and has permission
        # if not request.user.is_authenticated or not request.user.is_staff:
        #     return JsonResponse({"error": "Unauthorized"}, status=401)
        start_date = request.GET.get("start_date")
        end_date = request.GET.get("end_date")
        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="subscribers.csv"'

        writer = csv.writer(response)
        writer.writerow(["Name", "Email", "Subscribed At", "Active"])

        if all([start_date, end_date]):
            subscribers = Subscriber.objects.filter(
                subscribed_at__date__range=(start_date, end_date)
            )
        else:
            subscribers = Subscriber.objects.all()
            
        for subscriber in subscribers:
            writer.writerow(
                [
                    subscriber.name,
                    subscriber.email,
                    subscriber.subscribed_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "Yes" if subscriber.is_active else "No",
                ]
            )

        return response

class GetSubscribers(APIView):
    permission_classes = [IsAuthenticated & (IsAdmin | IsAgentAdmin | IsReadOnly)]
    
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
        ]
    )
    def get(self, request):
        start_date = request.GET.get("start_date", None)
        end_date = request.GET.get("end_date", None)
        
    
        if all([start_date, end_date]) and (start_date != "undefined" and end_date != "undefined"):
            subscribers = Subscriber.objects.filter(
                subscribed_at__date__range=(start_date, end_date)
            )
        else:
            subscribers = Subscriber.objects.all()
        
        return Response(
            api_response(
                message="Subscribers retrieved successfully", 
                status=True,
                data=SubscribersSerializer(subscribers, context={"request": request}, many=True).data
            )
        )

class CreateUserAPIView(APIView):
    permission_classes = [IsAuthenticated & (IsAdmin | IsAgentAdmin)]

    @swagger_auto_schema(
        request_body=UserSerializerIn
    )
    def post(self, request):
        status_, data = incoming_request_checks(request)

        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = UserSerializerIn(data=request.data, context={"request": request})
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        response = serializer.save()
        return Response(
            api_response(
                message="Account created successfully", status=True, data=response
            )
        )


class LoginAPIView(APIView):
    permission_classes = []


    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['email', 'password']
        )
    )
    def post(self, request):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        serializer = LoginSerializerIn(data=request.data, context={"request": request})
        serializer.is_valid() or raise_serializer_error_msg(errors=serializer.errors)
        user = serializer.save()
        return Response(
            api_response(
                message="Login successful",
                status=True,
                data={
                    "userData": UserSerializerOut(
                        user, context={"request": request}
                    ).data,
                    "accessToken": f"{AccessToken.for_user(user)}",
                    "refreshToken": f"{RefreshToken.for_user(user)}",
                },
            )
        )


class ChangePassword(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['old_password', 'password', 'confirm_password']
        )
    )
    def post(self, request):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        old_password = request.data.get("old_password")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        
        user : User = request.user
        

        if not user.check_password(old_password):
            return Response(
                api_response(message="Incorrect old password", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
            

        if password == confirm_password:
            try:
                validate_password(password)
            except Exception as e:
                return Response(
                api_response(message=" ".join(e), status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
            user.set_password(password)
            user.save()
            
            
            
            return Response(
                api_response(
                    message="Password changed successful",
                    status=True,
                    data={
                        "userData": UserSerializerOut(
                            user, context={"request": request}
                        ).data,
                    },
                )
            )
        
        return Response(
                api_response(message="Password doesnt match", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
            
  
class VerifyOtp(APIView):
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'otp': openapi.Schema(type=openapi.TYPE_STRING),
                'verification': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'otp', 'verification']
        )
    )
    def post(self, request):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        otp = request.data.get("otp")
        email = request.data.get("email")
        verify_type = request.data.get("verification", None)
        
        if not isinstance(otp, str):
            return Response(
                api_response(message="otp type is invalid", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            user = User.objects.get(email = email)
        except:
            return Response(
                api_response(message="User not found", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        userotp : UserOtp = user.otp
        
        if otp == userotp.otp and userotp.not_expired:
            if verify_type == "email":
                user.is_active = True
                user.save()
                
                userotp.delete()
            else:
                userotp.verified = True
                userotp.verification_type = verify_type
                userotp.verifiedOn = timezone.now()
                userotp.save()
            
            
            # userotp.delete()
            return Response(
                api_response(
                    message="Otp Verified successfully", status=True,
                    data={"otpverified": True, "email": email}
                )
            )
            
        
        return Response(
                api_response(message="otp is invalid or expired", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
class ResetPassword(APIView):
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING),
                'password': openapi.Schema(type=openapi.TYPE_STRING),
                'confirm_password': openapi.Schema(type=openapi.TYPE_STRING),
            },
            required=['email', 'password', 'confirm_password']
        )
    )
    def post(self, request):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        email = request.data.get("email")
        password = request.data.get("password")
        confirm_password = request.data.get("confirm_password")
        
        try:
            user = User.objects.get(email = email)
        except:
            return Response(
                api_response(message="User not found", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        userotp : UserOtp = user.otp
        
        if not userotp.verified:
            return Response(
                api_response(message="Otp verification required", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        if not userotp.not_verificationInvalid:
            userotp.delete()  
            return Response(
                api_response(message="Otp verification invalidated. Try again", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        if password == confirm_password:
            try:
                validate_password(password)
            except Exception as e:
                return Response(
                api_response(message=" ".join(e), status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
            user.set_password(password)
            user.save()
            
            try:
                userotp.delete()  
            except:
                pass
            
            return Response(
                api_response(
                    message="Password changed successful",
                    status=True,
                    data={
                        "userData": UserSerializerOut(
                            user, context={"request": request}
                        ).data,
                    },
                )
            )
        
        return Response(
                api_response(message="Password does not match", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )          


class RequestOtp(APIView):
    
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING)
            },
            required=['email']
        )
    )
    def post(self, request):
        status_, data = incoming_request_checks(request)
        if not status_:
            return Response(
                api_response(message=data, status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
            
        
        email = request.data.get("email")
        
        user = User.objects.filter(email=email).first()
        
        if not user:
            return Response(
                api_response(message="No user with this email", status=False),
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        
        if user:
            
            otp = UserOtp.objects.filter(
                    user__email = email
                ).first()
            
            if otp:
                otp.delete()
                
            otp = UserOtp.objects.create(
                user = user
            )
            
            context = {
                'subject':'OTP VERIFICATION',
                'body': f'This is your otp {otp.otp}',
                'otp': f'{otp.otp}'
            }
            
            sent, message = sendEmail(
                context,
                'otpemail.html',
                [email],
            )
            sendOTP = threading.Thread(target=sendEmail, args=[context, 'otpemail.html', [email]]).start()
            
                # return ("EMAIL SENT")
            
            #send otp here
            print("send otp ", otp.otp)
            return Response(
                api_response(message=f"Your otp is {otp.otp}",   # todo: remove otp
                            data={"email": email,},
                            status=True),
                status=status.HTTP_200_OK,
            )

        return Response(
            api_response(message="No acccount found with this email", status=False),
            status=status.HTTP_400_BAD_REQUEST,
        )
   