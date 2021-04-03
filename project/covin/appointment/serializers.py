from django.conf import settings
from rest_framework import serializers



class BookActionSerializer(serializers.Serializer):
    session_id = serializers.IntegerField()
    action = serializers.CharField()
    #content = serializers.CharField(allow_blank=True, required=False)