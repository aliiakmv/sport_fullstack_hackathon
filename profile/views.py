from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, ChangePasswordSerializer, ForgotPasswordSerializer, \
    ForgotPasswordCompleteSerializer, ActivationSerializer


User = get_user_model()


class RegisterApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


class ActivationApiView(ListAPIView):
    serializer_class = ActivationSerializer

    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Successfully', status=status.HTTP_200_OK)


class ChangePasswordApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsAuthenticated]


class ForgotPasswordApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ForgotPasswordSerializer


class ForgotPasswordCompleteApiView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ForgotPasswordCompleteSerializer



