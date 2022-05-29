from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from healthyfirst.api.models import Person


class PersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = [
            'username',
            'email',
            'groups',
            'first_name',
            'last_name',
            'password',
            'password2',
            'role',
            'id_area'
        ]

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=Person.objects.all())]
    )

    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if all(k in attrs for k in ("password", "password2")): # check if 'password' and 'password2' exist in attrs
            if attrs['password'] != attrs['password2']:
                raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = Person.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            role=validated_data['role'],
            id_area=validated_data['id_area'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    # def update(self, instance, validated_data):
    #     instance.email = validated_data.get('email', instance.email)
    #     # instance.content = validated_data.get('first', instance.content)
    #     # instance.created = validated_data.get('created', instance.created)
    #     instance.save()
    #     return instance


