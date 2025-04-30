# netbox_zabbix_plugin/api.py

from rest_framework import serializers
from ..models import DiscoveredHost

class DiscoveredHostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiscoveredHost
        fields = '__all__'
