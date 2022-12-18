from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from applications.account.serializers import RegisterSerializer, ForgotPasswordSerializer, \
    ForgotPasswordCompleteSerializer, ChangedPasswordSerializer, ChangedEmailSerializer

User = get_user_model()


class RegisterAPIView(APIView):

    @staticmethod
    def post(request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Your are successfully registered, we send a message to your email for activate user!')


class ActivationAPIView(APIView):

    @staticmethod
    def get(request, activation_code):
        try:
            user = User.objects.get(activation_code=activation_code)
            user.is_active = True
            user.activation_code = ''
            user.save()
            return Response('Successfully activate.', status=status.HTTP_201_CREATED)
        except User.DoesNotExist:
            return Response('Incorrect code!', status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordAPIView(APIView):

    @staticmethod
    def post(request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.send_code()
        return Response('We sent message to your email to insert your password.')


class ForgotPasswordCompleteAPIView(APIView):

    @staticmethod
    def post(request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Your password successfully updated!')


class ChangedPasswordAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = ChangedPasswordSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.set_new_password()
        return Response('Password successfully changed!')


class ChangedEmailAPIView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        serializer = ChangedEmailSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.changed_email()
        serializer.send_code()
        return Response('To verify the identity, activate the user by mail!')
