from rest_framework import serializers
from .models import User  # Import the custom User model

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    """
    This serializer is used to convert the User model instances to JSON and vice versa.
    It also ensures that the password is hashed when creating a new user.
    """
    
    class Meta:
        model = User  # Specify the model to be serialized (User model)
        # Fields that will be included in the serialized output or input
        fields = ['id', 'username', 'email', 'password']
        # We can also add `extra_kwargs` to customize behavior, for example:
        extra_kwargs = {
            'password': {'write_only': True}  # Prevent the password from being readable
        }

    def create(self, validated_data):
        """
        Custom create method to ensure the password is hashed before saving.
        
        Args:
            validated_data (dict): The validated data from the user input.

        Returns:
            User: The created User instance.
        """
        # Create a User instance using the validated data without saving yet
        user = User(**validated_data)
        # Hash the password using Django's set_password method
        user.set_password(validated_data['password'])
        # Save the user instance with the hashed password
        user.save()
        return user  # Return the newly created user