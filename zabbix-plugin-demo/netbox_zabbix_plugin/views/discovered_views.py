# netbox_zabbix_plugin/views/discovered_views.py

import logging
from django.shortcuts import get_object_or_404, render, redirect
from django.views import View
from django.urls import reverse
from utilities.views import ViewTab, register_model_view
from dcim.models import Device, DeviceRole, DeviceType, Site
from ipam.models import IPAddress
from netbox_zabbix_plugin.models import DiscoveredHost

logger = logging.getLogger('netbox_zabbix_plugin')

@register_model_view(
    DiscoveredHost,
    name='discoveredhost',       # ← this is the URL name that reverse() will use
    path='hosts'                 # ← URLs will be /plugins/zabbix/hosts/<pk>/
)
class DiscoveredHostView(View):
    """
    Detail view for a single DiscoveredHost.
    """
    queryset = DiscoveredHost.objects.all()
    model = DiscoveredHost
    permission = 'dcim.add_device'  # permission required to view this page
    tab   = ViewTab(label='Details')  # adds a “Details” tab

    def get(self, request, pk):
        host = get_object_or_404(DiscoveredHost, pk=pk)
        return render(request, 'netbox_zabbix_plugin/discoveredhost.html', {
            'object': host,             # NetBox page header
            'discoveredhost': host,     # for your template
        })
    def post(self, request, pk):
        host = get_object_or_404(DiscoveredHost, pk=pk)
        
        # does object exist in netbox
        
    
        existing = Device.objects.filter(name=host.name).first()
        if not existing and host.ip_address:
            existing = Device.objects.filter(
                primary_ip4__address__istartswith=host.ip_address
            ).first()

        if existing:
            return redirect('dcim:device', existing.pk)
        ip_obj = None
        if host.ip_address:
            ip_obj, _ = IPAddress.objects.get_or_create(
                address = f"{host.ip_address}/32" #TODO
            )
        # check what type of device role it is
        if host.os.__contains__("Linux"):
            role = DeviceRole.objects.get(name="Server")
        elif host.os.__contains__("Unknown"):
           #device role not set
            role = None
        params = {
            'name': host.name,
            'role': role.pk if role else None,
        }
        if ip_obj:
            params['primary_ip4'] = ip_obj.pk
            
        url = reverse('dcim:device_add')
        qs  = '&'.join(f"{k}={v}" for k,v in params.items())
        return redirect(f"{url}?{qs}")