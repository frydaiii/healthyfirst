from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from healthyfirst.api.models import Person, Certificate, Premise, BusinessType, InspectionPlan, Sample, Area


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
            'is_manager',
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
            is_manager=(validated_data['is_manager'] == 1),
            id_area=validated_data['id_area'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        if validated_data['password'] is not None or validated_data['password'] != '':
            user.set_password(validated_data['password'])
            user.save()
        return user


class PremiseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Premise
        fields = [
            'id',
            'name',
            'address',
            'phone_number',
            'id_area',
            'id_business_type',
            'id_certificate',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'id_certificate': {'required': False},
        }

    # def create(self, validated_data):
    #     if 'id_certificate' in validated_data:
    #         validated_data.pop('id_certificate')
    #     return super().create(validated_data)


class CertificateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certificate
        fields = [
            'id',
            'id_business_type',
            'issued_date',
            'expired_date',
            'series',
            'status',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
            'issued_date': {'read_only': True},
        }


class BusinessTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessType
        fields = [
            'id',
            'name',
            'description',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
        }


class InspectionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = InspectionPlan
        fields = [
            'id',
            'inspection_date',
            'sample_needed',
            'violate',
            'id_premise',
            'id_sample',
            'status',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
        }


class SampleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sample
        fields = [
            'id',
            'id_premise',
            'accreditation_premise',
            'accreditation_status',
            'result_date',
            'result_valid',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
        }


class AreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Area
        fields = [
            'id',
            'name',
            'type',
        ]
        extra_kwargs = {
            'id': {'read_only': True},
        }

