from rest_framework import serializers


class BlogSerializer(serializers.Serializer):
    id = serializers.CharField(read_only=True)
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    created_at = serializers.CharField(read_only=True)


class BlogUpdateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200, required=False)
    content = serializers.CharField(required=False)

    def validate(self, data):
        if not data:
            raise serializers.ValidationError("Provide at least one field to update.")
        return data