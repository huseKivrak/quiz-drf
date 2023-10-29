from dj_rest_auth.serializers import JWTSerializer


class CustomJWTSerializer(JWTSerializer):
    def to_representation(self, instance):
        data = super().to_representation(instance)
        del data['access']
        del data['refresh']
        return data
