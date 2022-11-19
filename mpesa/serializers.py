from rest_framework import serializers 
from .models import LipaNaMpesaOnline

class LipaNaMpesaSerializer(serializers.ModelSerializer):
    class Meta:
        model = LipaNaMpesaOnline
        fields = 'id'