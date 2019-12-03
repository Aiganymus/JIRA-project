from rest_framework import serializers
from users.models import MainUser, Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('bio', 'address', 'web_site', 'avatar')


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = MainUser
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        username = validated_data.get('username')
        password = validated_data.get('password')
        user = MainUser.objects.create_user(
            username=username,
            password=password
        )
        return user


class UserProfileSerializer(UserSerializer):
    profile = ProfileSerializer()

    class Meta(UserSerializer.Meta):
        fields = UserSerializer.Meta.fields + ('profile', )
