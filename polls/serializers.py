from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.validators import EmailValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import Poll, Option, Vote
from .utils import validate_email

# Polls
class OptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = ['id', 'text', 'vote_count']

class PollSerializer(serializers.ModelSerializer):
    options = OptionSerializer(many=True)

    class Meta:
        model = Poll
        fields = ['id', 'title', 'created_by', 'created_at', 'vote_count', 'options']
        read_only_fields = ['created_by', 'created_at', 'vote_count']

    # Make sure polls can only have 4 options max and a minimum of 2
    def validate_options(self, value):
        if len(value) < 2:
            raise serializers.ValidationError("A poll must have at least 2 options.")
        if len(value) > 4:
            raise serializers.ValidationError("A poll can have a maximum of 4 options.")
        return value
    

    def create(self, validated_data):
        # Grab the options data from the validated options so we don't pass through extra junk
        options_data = validated_data.pop('options')
        poll = Poll.objects.create(**validated_data)
        for option_data in options_data:
            Option.objects.create(poll=poll, **option_data)
        return poll


class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vote
        fields = ['id', 'poll', 'option', 'voted_by', 'created_at']
        read_only_fields = ['voted_by', 'created_at']

# User registration
class RegisterSerializer(serializers.ModelSerializer):
    # Validate password
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    # Validate email with regex
    email = serializers.EmailField(
        required=True,
        validators=[EmailValidator(message="Enter a valid email address.")],
    )
    # Grab IP address for ZeroBounce validation
    ip_address = serializers.IPAddressField(write_only=True, required=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'email', 'first_name', 'last_name', 'ip_address')

    def validate(self, attrs):
        # Validate password matching
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields do not match."})
        
        # Validate email with ZeroBounce
        ip_address = attrs.get('ip_address')
        if not validate_email(attrs['email'], ip_address):
            raise serializers.ValidationError({"email": "Email address is not valid."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        # This auto-salts and hashes the password
        user.set_password(validated_data['password'])

        # Save the user object
        user.save()

        return user

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token