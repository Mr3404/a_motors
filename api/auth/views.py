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
from django.core.cache import cache
from .serilializers import UserRegisterSerializer, UserProfileSerializer, UserProfileUpdateSerializer


class UserRegisterView(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        # 1. Validation Checks
        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)

        valid_domains = ["@gmail.com", "@yandex.ru", "@outlook.com", "@mail.ru", "@icloud.com"]
        if not any(domain in username for domain in valid_domains):
            return Response({"error": "Invalid email domain"}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            validate_password(password)
        except ValidationError as e:
            return Response({"error": e.messages}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Create User (Inactive)
        user = User.objects.create_user(username=username, password=password, is_active=False)

        # 3. Handle OTP (Stored in Cache)
        otp = random.randint(100000, 999999)
        cache.set(f"otp_{username}", otp, timeout=300)

        # 4. Send Email
        try:
            send_mail(
                'Your OTP Verification',
                f'Your OTP code is: {otp}',
                settings.EMAIL_HOST_USER,
                [username]
            )
            return Response({"message": "Check your email for OTP."}, status=status.HTTP_201_CREATED)
        except Exception as e:
            user.delete() # Cleanup if email fails
            return Response({"error": "Failed to send email. Try again later."}, status=500)

        # Fallback return (ensures we never return None)
        return Response({"error": "Internal server error"}, status=500)



# class VerifyOTPView(APIView):

#     def post(self, request):
#         username = request.data.get("username")
#         otp = request.data.get("otp")
#         try:
#             stored_otp = cache.get(f"otp_{username}")

#             if str(stored_otp) == str(otp):
#                 # Success: Activate the user
#                 user = User.objects.get(username=username)
#                 user.is_active = True
#                 user.save()

#                 # Important: Delete OTP after successful use
#                 cache.delete(f"otp_{username}")

#                 return Response({"message": "Account activated successfully!"}, status=200)
#         except:
#             return Response(status=404)from django.core.cache import cache

class VerifyOTPView(APIView):
    def post(self, request):
        username = request.data.get("username")
        otp = request.data.get("otp")

        # 1. Basic validation
        if not username or not otp:
            return Response({"error": "Username and OTP are required"}, status=status.HTTP_400_BAD_REQUEST)

        # 2. Retrieve from Cache
        stored_otp = cache.get(f"otp_{username}")

        # 3. Check if OTP exists/expired
        if stored_otp is None:
            return Response({"error": "OTP expired or never requested"}, status=status.HTTP_400_BAD_REQUEST)

        # 4. Compare OTPs
        if str(stored_otp) == str(otp):
            try:
                user = User.objects.get(username=username)
                user.is_active = True
                user.save()

                # Clean up cache
                cache.delete(f"otp_{username}")

                return Response({"message": "Account activated successfully!"}, status=status.HTTP_200_OK)
            except User.DoesNotExist:
                return Response({"error": "User no longer exists"}, status=status.HTTP_404_NOT_FOUND)

        # 5. Wrong OTP fallback
        return Response({"error": "Invalid OTP"}, status=status.HTTP_400_BAD_REQUEST)



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