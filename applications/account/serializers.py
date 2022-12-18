from django.contrib.auth import get_user_model
from rest_framework import serializers
from applications.account.tasks import send_confirmation_email, send_confirmation_code

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password_confirm = serializers.CharField(min_length=6, write_only=True, required=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'password_confirm']

    def validate(self, attrs):
        p1 = attrs.get('password')
        p2 = attrs.pop('password_confirm')

        if p1 != p2:
            raise serializers.ValidationError('Passwords dont same')

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        code = user.activation_code
        send_confirmation_email.delay(user.email, code)
        return user


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    @staticmethod
    def validate_email(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User does not exist')
        return email

    def send_code(self):
        email = self.validated_data.get('email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()
        send_confirmation_code.delay(email, user.activation_code)


class ForgotPasswordCompleteSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    code = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, min_length=6)
    password_confirm = serializers.CharField(required=True, min_length=6)

    @staticmethod
    def validated_email(email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User does not exist.')
        return email

    @staticmethod
    def validate_code(code):
        if not User.objects.filter(activation_code=code).exists():
            raise serializers.ValidationError('Incorrect code.')
        return code

    def validate(self, attrs):
        p1 = attrs.get('new_password')
        p2 = attrs.get('password_confirm')
        if p1 != p2:
            raise serializers.ValidationError('Passwords dont the same.')
        return attrs

    def set_new_password(self):
        email = self.validated_data.get('email')
        password = self.validated_data.get('new_password')
        user = User.objects.get(email=email)
        user.set_password(password)
        user.activation_code = ''
        user.save()


class ChangedPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, min_length=6)
    new_password = serializers.CharField(required=True, min_length=6)
    password_confirm = serializers.CharField(required=True, min_length=6)

    def validate(self, attrs):
        p1 = attrs.get('new_password')
        p2 = attrs.get('password_confirm')
        if p1 != p2:
            raise serializers.ValidationError('Passwords dont same.')
        return attrs

    def validate_old_password(self, password):
        request = self.context.get('request')
        user = request.user
        if not user.check_password(password):
            raise serializers.ValidationError('Incorrect password')
        return password

    def set_new_password(self):
        user = self.context.get('request').user
        password = self.validated_data.get('new_password')
        user.set_password(password)
        user.save()


class ChangedEmailSerializer(serializers.Serializer):
    new_email = serializers.EmailField(required=True)

    def changed_email(self):
        user = self.context.get('request').user
        user.email = self.validated_data.get('new_email')
        user.is_active = False
        user.save()

    def send_code(self):
        email = self.validated_data.get('new_email')
        user = User.objects.get(email=email)
        user.create_activation_code()
        user.save()
        send_confirmation_email.delay(email, user.activation_code)



