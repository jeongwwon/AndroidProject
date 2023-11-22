from blog.models import Post
from rest_framework import serializers


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'text', 'created_date', 'published_date', 'image','count')

class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    def validate(self, data):
        # You can add additional validation logic here if needed
        return data
