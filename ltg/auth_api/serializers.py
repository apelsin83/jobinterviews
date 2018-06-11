from django.contrib.auth import get_user_model
from rest_framework import serializers, exceptions

User = get_user_model()


class AuthSerializer(serializers.Serializer):

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    token = serializers.CharField()
    is_new = serializers.BooleanField()
    user_id = serializers.IntegerField()

    def _validate_token(self, token):
        if token:
            return token
        msg = _('Must include token.')
        raise exceptions.ValidationError(msg)

    def _validate_is_new(self, is_new):
        if is_new is None:
            msg = _('Wrong value for field is_new')
            raise exceptions.ValidationError(msg)
        return is_new

    def _validate_user_id(self, user_id):
        if user_id:
            return user_id
        msg = _('Wrong value for field user_id')
        raise exceptions.ValidationError(msg)

    def validate(self, attrs):

        token = attrs.get('token')
        is_new = attrs.get('is_new')
        user_id = attrs.get('user_id')

        self._validate_token(token)
        self._validate_is_new(is_new)
        self._validate_user_id(user_id)
        return attrs

