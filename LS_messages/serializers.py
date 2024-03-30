from rest_framework import serializers

from .models import Message  # Import the Message model


class MessageSerializer(serializers.ModelSerializer):
    """
    Serializer for the Message model.

    This class is used to convert the Message model instances into
    JSON format.
    """

    class Meta:
        """
        Meta class for MessageSerializer.

        This class contains metadata for the MessageSerializer.
        The 'model' attribute specifies the model to be used
        and the 'fields' attribute specifies which fields to include in
        the JSON representation of the model.
        """

        model = Message  # The model to be used
        fields = "__all__"  # Include all fields in the JSON representation
