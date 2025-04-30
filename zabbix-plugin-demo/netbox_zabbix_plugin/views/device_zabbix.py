# netbox_zabbix_plugin/views/device_views.py

import logging
from django.shortcuts import get_object_or_404, render
from django.views import View
from dcim.models import Device
from utilities.views import ViewTab, register_model_view
from netbox.plugins import get_plugin_config
from netbox_zabbix_plugin.api_request import API_request

logger = logging.getLogger('netbox_zabbix_plugin')

@register_model_view(Device, name="zabbix", path="zabbix")
class DeviceZabbixView(View):
    """
    Renders a “Zabbix” tab on the Device page, linking through to
    the Zabbix host dashboard for this device’s primary IP.
    """
    model = Device
    tab = ViewTab(label="Zabbix", permission="dcim.view_device")

    def _get_hostid_for_ip(self, ip):
        """
        Look up the Zabbix hostid by filtering hostinterface.ip via JSON-RPC.
        """
        result = API_request._zabbix_api_request({
            "jsonrpc": "2.0",
            "method":  "hostinterface.get",
            "params": {
                "output": ["hostid"],
                "search": {"ip": ip}
            },
            "id": 1
        })
        return result[0]["hostid"] if result else None
    
    def get(self, request, pk):
        device = get_object_or_404(Device, pk=pk)
        ip = device.primary_ip.address.ip if device.primary_ip else None
        hostid =  hostid = ip and self._get_hostid_for_ip(str(ip))
        base = get_plugin_config('netbox_zabbix_plugin', 'zabbix_url').rstrip('/')
        zlink = hostid and f"{base}/zabbix.php?action=host.dashboard.view&hostid={hostid}"
        return render(request, 'netbox_zabbix_plugin/device_zabbix.html', {
            'object':        device,         # NetBox header / breadcrumbs
            'device':        device,         # your template can still inspect .primary_ip
            'zabbix_link':   zlink,          # dashboard URL
            'tab':           self.tab,       # ensure the “Zabbix” tab stays selected
        })