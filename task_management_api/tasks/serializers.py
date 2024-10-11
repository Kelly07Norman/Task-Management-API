from rest_framework import serializers
from .models import Task
from categories.models import TaskCategory
from django.utils.timezone import make_aware
from django.utils import timezone
from datetime import datetime, time, date

class TaskSerializer(serializers.ModelSerializer):
    """
    Serializer for the Task model.
    Handles validation, serialization, and creation of Task objects.
    """
    # Use PrimaryKeyRelatedField for category to link the task to a category by its ID
    category = serializers.PrimaryKeyRelatedField(queryset=TaskCategory.objects.all())  
    priority = serializers.CharField(required=True)  # Make priority a required field

    class Meta:
        model = Task  # This serializer is based on the Task model
        fields = [
            'id', 'title', 'description', 'due_date', 'priority', 'status', 
            'category', 'created_at', 'updated_at', 'user', 'is_completed'
        ]  # Specify the fields to be serialized
        read_only_fields = ['user']  # Prevent the user field from being editable

    # Custom validation for due_date
    def validate_due_date(self, value):
        """
        Ensure the due_date is in the present or future.
        Also accepts dates in 'dd-mm-yyyy' format and ensures the date is timezone-aware.
        """
        if isinstance(value, str):
            try:
                # Parse date string in 'dd-mm-yyyy' format to a date object
                value = datetime.strptime(value, "%d-%m-%Y").date()
            except ValueError:
                raise serializers.ValidationError("Date format must be dd-mm-yyyy.")
        
        # Convert date to datetime if necessary
        if isinstance(value, date) and not isinstance(value, datetime):
            value = datetime.combine(value, time.min)

        # Ensure the datetime is timezone-aware
        if value.tzinfo is None:
            value = make_aware(value)

        # Get current time and check if the due_date is in the past
        current_time = timezone.now()
        if value < current_time.replace(hour=0, minute=0, second=0, microsecond=0):
            raise serializers.ValidationError("The due date cannot be in the past.")
        
        return value  # Return the valid due_date

    def create(self, validated_data):
        """
        Automatically associate the user with the task during creation.
        """
        validated_data['user'] = self.context['request'].user  # Associate the authenticated user
        return super().create(validated_data)

    def update(self, instance, validated_data):
        """
        Update the task with any new data provided.
        """
        # Update the fields if new data is provided, otherwise retain the old values
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.due_date = validated_data.get('due_date', instance.due_date)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.status = validated_data.get('status', instance.status)
        instance.category = validated_data.get('category', instance.category)
        instance.save()  # Save the updated instance
        return instance

    def to_representation(self, instance):
        """
        Customize how the Task instance is represented when returned as a response.
        """
        representation = super().to_representation(instance)

        # Format created_at and updated_at fields to be more readable
        representation['created_at'] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S")
        representation['updated_at'] = instance.updated_at.strftime("%Y-%m-%d %H:%M:%S")

        # Format the due_date in a more user-friendly way
        if instance.due_date:
            representation['due_date'] = instance.due_date.strftime("%B %d, %Y")  # Example: October 01, 2024
        else:
            representation['due_date'] = None  # Handle case where due_date might be None

        # Show the category's name instead of the category ID
        representation['category'] = instance.category.name if instance.category else None

        return representation  # Return the customized representation