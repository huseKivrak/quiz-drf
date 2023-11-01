from dj_rest_auth.serializers import JWTSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers


class CustomJWTSerializer(JWTSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data['access']
        del data['refresh']
        return data


class CustomRegisterSerializer(RegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(
        required=False, allow_blank=True, default='')

    def get_cleaned_data(self):
        data_dict = super().get_cleaned_data()
        data_dict['first_name'] = self.validated_data.get('first_name', '')
        data_dict['last_name'] = self.validated_data.get('last_name', '')
        return data_dict

    def save(self, request):
        user = super().save(request)
        user.first_name = self.data.get('first_name')
        user.last_name = self.data.get('last_name')
        user.save()
        return user
