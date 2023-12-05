from blog.models import Post
from blog.models import GlobalPostCount
from rest_framework import serializers

class GlobalPostCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalPostCount
        fields = ('count')

class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text', 'created_date', 'published_date', 'image','count')

class PostSerializer2(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('published_date', 'text')  # Exclude 'image' field as it will be handled separately

    def to_representation(self, instance):
        # Get the base URL from the request
        base_url = self.context['request'].build_absolute_uri('/')

        # Create a dictionary with the fields from the model
        representation = super().to_representation(instance)

        # Add the base URL to the 'image' field if it exists
        if instance.image:
            representation['image'] = f"{base_url}{instance.image.url}"

        return representation

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate(self, data):
        # You can add additional validation logic here if needed
        return data
