from knox.models import AuthToken
from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT
from rest_framework.views import APIView

from accounts.serializers import LoginSerializer, RegisterSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, req):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({
            "message": "Registration Successful",
            "user": RegisterSerializer(user).data,
        }, status=HTTP_201_CREATED)


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, req):
        serializer = self.get_serializer(data=req.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = AuthToken.objects.create(user)[1]


        return Response({
            "message": "Login Successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "username": user.username,
                "token": token
            }
        }, status=HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, req):
        req.auth.delete()
        return Response({
            "message": "Logout Successful"
        }, status=HTTP_204_NO_CONTENT)

