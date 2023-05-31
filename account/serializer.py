from rest_framework import serializers
from .models import Account
from rest_framework.exceptions import AuthenticationFailed, ValidationError
from django.contrib.auth import authenticate


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=8, max_length=88, write_only=True)
    password2 = serializers.CharField(min_length=8, max_length=88, write_only=True)

    class Meta:
        model = Account
        fields = ('email', 'password', 'password2')

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        if password != password2:
            raise ValidationError({'muvaffaqiyat': False, 'xabar': 'Parol mos kelmadi!'})
        return attrs

    def create(self, validated_data):
        del validated_data['password2']
        return Account.objects.create_user(**validated_data)


class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(min_length=8, max_length=88, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def get_tokens(self, obj):
        email = obj.get('email')
        tokens = Account.objects.get(email=email).tokens
        return tokens

    class Meta:
        model = Account
        fields = ('email', 'password', 'tokens')

    def validate(self, attrs):
        password = attrs.get('password')
        email = attrs.get('email')
        user = authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed({
                'xabar': 'Email yoki Parol xato'
            })
        if not user.is_active:
            raise AuthenticationFailed({
                'xabar': 'Hisob faol eams'
            })
        return attrs


class MyAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'email', 'full_name', 'image', 'is_superuser', 'is_active', 'is_staff', 'create_date')


class MyAccountResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'email', 'full_name', 'image')


class MyAccountUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('id', 'email', 'full_name', 'image',)
        extra_kwargs = {
            'full_name': {'required': False}
        }




