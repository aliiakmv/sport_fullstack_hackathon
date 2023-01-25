from django.contrib.auth import get_user_model
from rest_framework import serializers

from .send_mail import send_activation_email, send_confirmation_code

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password', 'password_confirm']

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password_confirm')
        if p1 != p2:
            raise serializers.ValidationError('Wrong password')
        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        code = user.activation_code
        send_activation_email(user.email, code)

        return user


class ActivationSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = 'all'


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, min_length=6, write_only=True)
    new_password_confirm = serializers.CharField(required=True, min_length=6, write_only=True)

    def validate(self, attrs):
        p1 = attrs.get('new_password')
        p2 = attrs.get('new_password_confirm')
        if p1 != p2:
            raise serializers.ValidationError('Passwords do not match, please try again')
        return attrs

    def validate_old_password(self, attrs):
        user = self.context.get('request').user
        if not user.check_password(attrs):
            raise serializers.ValidationError('Wrong old password')
        return attrs

    def create(self, validated_data):
        user = self.context.get('request').user
        password = self.validated_data.get('new_password')
        user.set_password(password)
        user.save()
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validated_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This user is not found in our database')
        return email

    def create(self, validated_data):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()
        send_confirmation_code(email, user.activation_code)
        return user


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, min_length=6, write_only=True)
    password_confirm = serializers.CharField(required=True, min_length=6, write_only=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('This user is not found in our database.')
        return email

    def validate_code(self, code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Incorrect activation code')
        return code

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.get('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError('Passwords do not match, please try again')
        return attrs

    def create(self, validated_data):
        email = self.validated_data.get('email')
        password = self.validated_data.get('password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()
        return user
