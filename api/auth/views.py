from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings
import random
from .serilializers import UserRegisterSerializer, UserProfileSerializer, UserProfileUpdateSerializer


class UserRegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not any(domain in username for domain in ["@gmail.com", "@yandex.ru", "@outlook.com", "@mail.ru", "@icloud.com"]):
            return Response(
                {"error": "Username must be an email address from a valid domain"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if not username or not password:
            return Response(
                {"error": "Username and password required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if User.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(password)
        except ValidationError as e:
            return Response(
                {"error": e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.create_user(
            username=username,
            password=password,
            is_active=False
        )
        otp = random.randint(100000, 999999)
        subject = 'Your OTP Verification'
        message = f'Your OTP code is: {otp}'
        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [username])
            return Response(
                {"message": "User registered successfully. Please check your email for the OTP."},
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            user.delete()
            return Response(
                {"error": "Failed to send OTP email. Please try again."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class VerifyOTPView(APIView):

    def post(self, request):
        username = request.data.get("username")
        otp = request.data.get("otp")

        if not username or not otp:
            return Response(
                {"error": "Username and OTP required"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = User.objects.get(username=username)
            user.is_active = True
            user.save()
            refresh = RefreshToken.for_user(user)

            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh)
            }, status=status.HTTP_200_OK)

        except User.DoesNotExist:
            return Response(
                {"error": "User does not exist"},
                status=status.HTTP_404_NOT_FOUND
            )
                
        
class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            serializer = UserProfileSerializer(request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def put(self, request):
        try:
            serializer = UserProfileUpdateSerializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)