from django.contrib.postgres.fields import ArrayField
from django.db import models
from netbox.models import NetBoxModel
from django.urls import reverse


class DiscoveredHost(NetBoxModel):
    """
    Represents a discovered host in Zabbix.
    """
    name = models.CharField(max_length=255, unique=True)
    ip_address = models.GenericIPAddressField()
    hostid = models.CharField(max_length=255, unique=True)
    tags = ArrayField(models.CharField(max_length=255), blank=True, default=list)
    os = models.CharField(max_length=255, blank=True)
    

    class Meta:
        ordering = ['name']
        verbose_name = 'Discovered Host'
        verbose_name_plural = 'Discovered Hosts'

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('plugins:netbox_zabbix_plugin:discoveredhost', args=[self.pk])