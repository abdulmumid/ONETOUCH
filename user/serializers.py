from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import OTP, MycarProfile, Avatar

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "phone", "password", "confirm_password"]

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Пользователь с этим email уже существует")
        return value

    def validate_phone(self, value):
        if User.objects.filter(phone=value).exists():
            raise serializers.ValidationError("Пользователь с этим номером уже существует")
        return value

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Пароли не совпадают")
        return data

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        user = User.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            phone=validated_data.get("phone")
        )
        OTP.create_otp(user, purpose="registration")
        return user


class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        otp = OTP.objects.filter(
            user=user, code=data["code"], is_used=False, purpose="registration"
        ).order_by("-created_at").first()

        if not otp:
            raise serializers.ValidationError("Неверный код")
        if otp.is_expired():
            raise serializers.ValidationError("Код просрочен")

        data["user"] = user
        data["otp"] = otp
        return data

    def save(self):
        user = self.validated_data["user"]
        otp = self.validated_data["otp"]
        user.is_verified = True
        user.save()
        otp.is_used = True
        otp.save()
        return user


class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        if user.is_verified:
            raise serializers.ValidationError("Email уже подтверждён")

        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        otp = OTP.create_otp(user, purpose="registration")
        return {"user": user, "otp": otp}


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        if not user.check_password(data["password"]):
            raise serializers.ValidationError("Неверный пароль")

        data["user"] = user
        return data


class PlayerIdSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["player_id"]


class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate(self, data):
        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")
        data["user"] = user
        return data

    def save(self):
        user = self.validated_data["user"]
        OTP.create_otp(user, purpose="reset_password")
        return user


class ResetPasswordConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(max_length=6)
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data["password"] != data["confirm_password"]:
            raise serializers.ValidationError("Пароли не совпадают")

        try:
            user = User.objects.get(email=data["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError("Пользователь не найден")

        otp = OTP.objects.filter(
            user=user, code=data["code"], is_used=False, purpose="reset_password"
        ).order_by("-created_at").first()

        if not otp:
            raise serializers.ValidationError("Неверный код")
        if otp.is_expired():
            raise serializers.ValidationError("Код просрочен")

        data["user"] = user
        data["otp"] = otp
        return data

    def save(self):
        user = self.validated_data["user"]
        otp = self.validated_data["otp"]
        user.set_password(self.validated_data["password"])
        user.save()
        otp.is_used = True
        otp.save()
        return user


# --- Обновление профиля ---
class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["first_name", "phone"]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "phone", "is_verified", "player_id"]


class MycarProfileSerializer(serializers.ModelSerializer):
    marka = serializers.StringRelatedField()  
    model = serializers.StringRelatedField()  
    body = serializers.StringRelatedField()   

    class Meta:
        model = MycarProfile
        fields = ['id', 'user', 'marka', 'model', 'body', 'gos_number']
        read_only_fields = ['user']


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = "__all__"