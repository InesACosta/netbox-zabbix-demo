# netbox_zabbix_plugin/views/home.py

import logging
from django.views.generic import TemplateView
from django_tables2 import RequestConfig
from .device_zabbix import DeviceZabbixView
from netbox_zabbix_plugin.models import DiscoveredHost
from netbox_zabbix_plugin.tables import DiscoveredHostTable
from netbox_zabbix_plugin.api_request import API_request

logger = logging.getLogger('netbox_zabbix_plugin')

class ZabbixHomeView(TemplateView):
    template_name = 'netbox_zabbix_plugin/home.html'

    def _fetch_and_save_discovered_hosts(self):
        """
        Fetch all discovered hosts from the Zabbix API and upsert them.
        """
        result = API_request._zabbix_api_request({
            "jsonrpc": "2.0",
            "method":  "host.get",
            "params": {
                "output": ["hostid", "name"],
                "selectInterfaces": ["ip"]
            },
            "id": 1
        })
                
        for host in result:
            ip = host["interfaces"][0]["ip"] if host["interfaces"] else None
            host_details = self._get_host_details(host["hostid"])
            inventory = host_details.get('inventory', {})
            host["os"] = inventory.get('os','') if inventory else 'Unknown'
            DiscoveredHost.objects.update_or_create(
                hostid=host["hostid"],
                defaults={
                    "name":       host["name"],
                    "ip_address": ip,
                    "tags":       host.get("tags", []),
                    "os":       host["os"],
                }
            )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            self._fetch_and_save_discovered_hosts()
        except Exception as e:
            logger.error("Error fetching Zabbix hosts: %s", e)

        qs = DiscoveredHost.objects.all().order_by('hostid')
        table = DiscoveredHostTable(qs)
        RequestConfig(self.request, paginate={'per_page': 50}).configure(table)
        context['table'] = table

        return context
    
    
    def _get_host_details(self, hostid):
        """
        Pull in interfaces, inventory, groups and parent templates.
        """
        results = API_request._zabbix_api_request({
            "jsonrpc": "2.0",
            "method":  "host.get",
            "params": {
                "hostids": [hostid],
                "output": ["hostid", "name"],
                "selectInterfaces": ["ip"],
                "selectInventory": "extend",
                "selectGroups": ["groupid","name"],
                "selectParentTemplates": ["templateid","name"],
            },
            "id": 2
        })
        return (results[0] if results else {})
    
