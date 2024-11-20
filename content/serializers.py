from rest_framework import serializers
from .models import User , users

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'age')


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()

class RegisterSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField()
    age=serializers.IntegerField()

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            age=validated_data['age']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    class Meta:
        model = User
        fields = ['email' , 'password' , 'age']

class ShowSerializer(serializers.Serializer):
    show_id = serializers.CharField()
    type = serializers.CharField()
    title = serializers.CharField()
    director = serializers.CharField()
    cast = serializers.CharField()
    country = serializers.CharField()
    date_added = serializers.CharField()
    release_year = serializers.CharField()
    rating = serializers.CharField()
    duration = serializers.CharField()
    listed_in = serializers.CharField()
    description = serializers.CharField()
