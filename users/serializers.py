from rest_framework import serializers
from .models import User, Profile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username', 'email', 'phone', 'password')

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            phone=validated_data['phone'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user
    

class ProfileSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    resume = serializers.FileField(required=False)
    class Meta:
        model = Profile
        fields = ('about', 'image', 'resume')


